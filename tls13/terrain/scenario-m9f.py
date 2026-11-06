#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-m9f.py — LE TERRAIN M9-(f) : LA SESSION RÉELLE, LA GRANDE ŒUVRE.

Le kit porte UN artefact et UN scénario :
  proxy.exe   le build 1.0.0-dev.2 du jalon M9 — 65 024 o, sha256
              d892893469608fd69e381b92b8e18623107bd2bc694f43a512bc5900773dc314
              (lecture seule pour le run — le scénario ne l'écrit JAMAIS ;
              la carte privée ne voyage JAMAIS avec l'artefact, R1) ;
  le présent script — python SEUL (ctypes, hashlib, os, platform, socket,
              struct, sys, threading, time — AUCUN paquet à installer).

CE QUE LE RUN DÉMONTRE (chaque constat tranché binaire, le verdict
POST-MORTEM — un échec nommé vaut plus qu'un vert muet) :

  T0 LE TÉMOIN    l'empreinte de l'artefact ASSERTÉE avant tout geste ;
                 l'environnement consigné (Windows, Python 64 bits) ; le
                 VRAI ntdll localisé et son fichier haché ; l'artefact
                 cartographié (LoadLibraryEx DONT_RESOLVE — le scénario
                 est le chargeur, jamais l'exécutant de l'artefact
                 entier) ; les octets attendus constatés UN PAR UN (le
                 trombone sys-01, les fixtures transport AFD, l'OCTET
                 DE LONGUEUR DU RECORD CH — l'erratum n° 5 relu dans
                 l'image, les slots scellés) ; la cible résolue (DNS) et
                 l'EMPREINTE ÉPINGLÉE consignée.
  T1 LA RÉSOLUTION le VRAI ntdll lu par DEUX lecteurs indépendants : la
                 marche EAT refaite en PYTHON et le BLOC sys-02 (le code
                 de l'artefact, appelé à son adresse scellée) — LE MÊME
                 SSN pour les trois noms du transport (NtCreateFile,
                 NtDeviceIoControlFile, NtClose) ; le MOTIF du stub
                 confronté (4C 8B D1 B8 avant l'imm32 — un stub
                 crocheté est un REFUS NOMMÉ).
  T2 L'ÉTABLISSEMENT le socket TCP par le VRAI afd.sys : sys-04 appelé à
                 son adresse scellée (NtCreateFile \Device\Afd\Endpoint,
                 bind implicite WILDCARD, connect SYNCHRONE — TROIS
                 appels NT, chaque SSN résolu AU GESTE MÊME par sys-02) ;
                 JAMAIS ws2_32 (la surface de hook que M8 a nommée).
  T3 LA SESSION   LA POIGNÉE ENTIÈRE par LE CLIENT TLS 1.3 DE
                 L'ARTEFACT : tls13-27 (la machine d'états) appelée à son
                 adresse scellée, le socle tls13-28 câblé aux rappels DU
                 KIT (chaque octet émis part par sys-05, chaque octet
                 reçu arrive par sys-06 — les SYSCALLS DIRECTS, jamais
                 l'IAT) ; le kit fournit TOUT : l'aléa, le couple
                 x25519, L'EMPREINTE ÉPINGLÉE ; LE RECOUP : le
                 ClientHello émis par la machine == la construction
                 re-jouée en Python pur (16 03 03 00 72 || 114 o, l'aléa
                 du kit @ +6, la clé publique @ +82 — l'échelle
                 RFC 7748 refaite en Python : les DEUX lecteurs encore).
  T4 LA LIGNE     LA LIGNE APPLICATIVE CHIFFRÉE ÉCHANGÉE : É2 ÉMETTRE —
                 le GET HTTP scellé par LA MACHINE sous SES clés ; É3
                 RECEVOIR — la réponse reçue, DÉCHIFFRÉE PAR LA MACHINE,
                 le témoin « HTTP/1.1 200 OK » cherché dans le flux en
                 clair restitué (les tickets de session éventuels
                 traversent comme données — ignorés) ; la ligne reçue
                 sauvée comme pièce.
  T5 L'ÉPINGLAGE  LA FALSIFICATION CONTRE LE VRAI SERVEUR : une seconde
                 session, L'EMPREINTE MUTÉE d'un bit → le certificat
                 réel offert N'EST PAS celui qu'on attend → -6 NOMMÉ
                 (l'épinglage divergent), l'état 5 (MORT), le journal ==
                 l'offre seule — la confiance est une COMPARAISON, la
                 garde constatée sur le monde réel.
  T6 LA CLÔTURE   É4 FERMER : le close_notify composé et scellé PAR LA
                 MACHINE (24 o) ; puis la fermeture des handles — LE
                 GESTE DU KIT (I8 de sys-04) : NtClose résolu par
                 sys-02, ÉMIS PAR SYS-01 (le trombone, via un trampoline
                 à deux instructions — ctypes ne peut pas charger rax,
                 le trampoline le fait) ; l'artefact relu inchangé, la
                 cartographie libérée.
  T7 LE VERDICT   VERDICT-run-m9f.txt — VERT si le critère tient : LA
                 SESSION RÉELLE, LE VRAI ntdll, LES SOCKETS PAR
                 SYSCALLS, L'ÉPINGLAGE, LA LIGNE CHIFFRÉE ÉCHANGÉE.

Les pièces naissent toutes seules dans ./preuves-m9f/ :
  temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt,
  ligne-recue.txt, journal-emissions.txt
— à renvoyer ENTIÈRES au coffre /test/preuves-m9f/ (dossier Drive
« Triade » → « test »). Le laboratoire recoupe sur pièces (D138/D145/
D148) et, si elles établissent le critère, la finale 1.0.0 est posée
(fait de carte, D104) : le jalon M9 franchi — LA GRANDE ŒUVRE.

Un verdict ÉCHEC NOMMÉ se renvoie TEL QUEL : la ligne nomme le défaut.
NOTE D'HONNÊTETÉ : l'empreinte épinglée est celle du certificat servi
par www.cloudflare.com SANS SNI (le ClientHello du jalon n'en porte
pas — I3 de tls13-22 : « le kit cible le serveur par son adresse,
l'épinglage fait la confiance ») : un certificat renouvelé côté serveur
fera échouer T3 par -6 NOMMÉ — c'est la NATURE de l'épinglage, pas une
panne du kit ; renvoyez les pièces, le labo re-gèle l'empreinte.
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
PREUVES = os.path.join(ICI, "preuves-m9f")

# --- l'artefact : la carte génération 10 prouve CES octets -----------------------
SHA_PROXY = ("d892893469608fd69e381b92b8e18623107bd2bc694f43a512"
             "bc5900773dc314")
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
R_TETE_CH = 0x10082      # l'écriture de l'en-tête du record CH dans
                         # tls13-27 (12 o : mov dword + mov byte — l'octet
                         # de longueur 0x72 DE L'ERRATUM n° 5 relu ici)

OCTETS_SYS01 = bytes.fromhex("4989ca0f05c3")   # mov r10,rcx; syscall; ret
OCTETS_TETE_CH = bytes.fromhex("41c7021603030041c6420472")
NOM_DEVICE = "\\Device\\Afd\\Endpoint"     # le nom du périphérique AFD
FIXTURE_DEVICE = NOM_DEVICE.encode("utf-16le") + b"\x00\x00"   # 42 o
MOTIF_STUB = bytes.fromhex("4c8bd1b8")        # mov r10,rcx ; mov eax —

# --- la session : les dimensions DÉCLARÉES (tls13-27 P1) ------------------------
SESSION_TAILLE = 17520     # le contexte session
KIT96 = 96                 # aléa 32 + clé privée 32 + empreinte attendue 32
SOCLE_TAILLE = 32          # émettre ptr/ctx + recevoir ptr/ctx (tls13-28 P1)
TAMPOIN_CAPACITE = 16500  # ≥ 5 + 2^14 + 17 (É3 : l'enregistrement ENTIER)

# --- LA CIBLE ET LA CONFIANCE DU KIT (figées au laboratoire le 06/11) -----------
CIBLE = "www.cloudflare.com"
CIBLE_PORT = 443
# Le certificat de l'entité servi SANS SNI par la cible — CN=www.cloudflare.com,
# émis par Let's Encrypt (YR2), RSA-2048, valide 2026-11-01 → 2027-01-30 —
# l'empreinte ÉPINGLÉE (sha256 du DER, le DÉTROIT de tls13-26) :
EMPREINTE_EPINGLEE = bytes.fromhex(
    "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f")
TEMOIN_APPLICATIF = b"HTTP/1.1 200 OK"
LIGNE_EMISE = (f"GET / HTTP/1.1\r\nHost: {CIBLE}\r\n"
               f"User-Agent: TRIADE-M9-terrain\r\nConnection: close\r\n\r\n"
               ).encode("ascii")

# la construction re-jouée du CH (le recoup : les DEUX lecteurs)
CH_TAILLE = 114
CH_RECORD = bytes.fromhex("1603030072")    # type 22, 0x0303, longueur 114

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
        with open(os.path.join(PREUVES, "scenario-m9f-journal.log"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(_journal) + "\n")
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
    """La marche EAT refaite en Python : (code, rva_stub, detail) — LE MÊME
    contrat que sys-02 (la fenêtre e_lfanew, le motif PE, le répertoire
    export, la marche BORNÉE, le motif du stub AVANT l'imm32)."""
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
    Rend (ssn, stub_rva) ou lève RefusNomme."""
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
    """L'échelle de Montgomery EN PUR PYTHON — le second lecteur du couple
    (le premier est tls13-14, dans l'artefact)."""
    p = 2 ** 255 - 19

    def cswap(swap, a, b):
        return (b, a) if swap else (a, b)

    k = int.from_bytes(priv, "little")
    k &= (1 << 254) - 8
    k |= 1 << 254
    x1 = point_base
    x2, z2, x3, z3 = 1, 0, 0, 1
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
        z2 = e * (aa + ((p + 1) // 4) * e) % p
    x2, x3 = cswap(swap, x2, x3)
    z2, z3 = cswap(swap, z2, z3)
    return (x2 * pow(z2, p - 2, p) % p).to_bytes(32, "little")


def construction_ch_reference(alea, cle_publique):
    """La construction re-jouée du plan (114 o FIXES) — le recoup de
    l'OFFRE composée par la machine."""
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


# --- la garde-chien (un transport muet est une information, pas une attente) ----

def _garde_chien():
    journal("LA GARDE-CHIEN : 300 s écoulées — le transport est muet ; "
            "les pièces écrites à l'instant demeurent, fermez la fenêtre "
            "et renvoyez preuves-m9f/ TEL QUELLE (un échec nommé vaut "
            "plus qu'un vert muet)")
    os._exit(3)


def armer_garde_chien():
    t = threading.Timer(300.0, _garde_chien)
    t.daemon = True
    t.start()


# --- LE RUN ----------------------------------------------------------------------

class RefusNomme(RuntimeError):
    pass


def main():
    print("=== LE TERRAIN M9-(f) : LA SESSION RÉELLE — LA GRANDE ŒUVRE ===\n")
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
        print(f"ÉCHEC NOMMÉ : ce terrain exige Windows (sys.platform="
              f"{sys.platform!r}) — le VRAI ntdll et le VRAI afd.sys")
        return 1
    if struct.calcsize("P") != 8:
        print("ÉCHEC NOMMÉ : ce terrain exige un Python 64 bits "
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

    # la cartographie : DONT_RESOLVE — aucune entrée résolue, AUCUN point
    # d'entrée appelé ; le scénario est le CHARGEUR, jamais l'exécutant
    # de l'artefact entier
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

    # les octets attendus, constatés UN PAR UN (la carte génération 10
    # lue sur la machine réelle)
    verifie("T0.sys-01 : le trombone ABI",
            ctypes.string_at(base + R_SYS01, 6) == OCTETS_SYS01,
            f"{ctypes.string_at(base + R_SYS01, 6).hex()}")
    verifie("T0.fixture-device : le périphérique AFD UTF-16LE + NUL",
            ctypes.string_at(base + R_SYS_DEVICE, 42) == FIXTURE_DEVICE,
            f"{NOM_DEVICE} — {len(FIXTURE_DEVICE)} o")
    for rva, nom in ((R_SYS_NOM_CREATEFILE, "NtCreateFile"),
                     (R_SYS_NOM_DEVICEIOCTL, "NtDeviceIoControlFile"),
                     (R_SYS_NOM_CLOSE, "NtClose")):
        verifie(f"T0.fixture-span : « {nom} »",
                ctypes.string_at(base + rva, len(nom)) == nom.encode(),
                f"@{rva:#x}")
    # L'OCTET DE L'ERRATUM n° 5 relu dans l'image : l'en-tête du record
    # CH (16 03 03 00 72) écrite par tls13-27 — le kit embarque la
    # PREUVE que l'octet réparé est dans CES octets
    verifie("T0.erratum-5 : l'octet de longueur du record CH relu "
            "(41 C7 02 16 03 03 00 41 C6 42 04 72)",
            ctypes.string_at(base + R_TETE_CH, 12) == OCTETS_TETE_CH,
            f"@{R_TETE_CH:#x}")
    # les têtes des slots scellés (le constat que le plan vit dans l'image)
    for rva, nom in ((R_SYS02, "sys-02"), (R_SYS04, "sys-04"),
                     (R_SYS05, "sys-05"), (R_SYS06, "sys-06"),
                     (R_TLS27, "tls13-27"), (R_TLS28, "tls13-28")):
        tete = ctypes.string_at(base + rva, 6)
        verifie(f"T0.slot : la tête {nom} @{rva:#x}",
                tete != b"\x00" * 6 and tete != b"\xcc" * 6, tete.hex())

    # la cible résolue (le kit cible le serveur PAR SON ADRESSE — I3)
    infos = socket.getaddrinfo(CIBLE, CIBLE_PORT, socket.AF_INET,
                               socket.SOCK_STREAM)
    ip_cible = infos[0][4][0]
    temoin(f"[cible] {CIBLE}:{CIBLE_PORT} → {ip_cible} (DNS résolu au run)")
    temoin(f"[cible] l'empreinte ÉPINGLÉE : {EMPREINTE_EPINGLEE.hex()}")
    temoin(f"[cible] le témoin applicatif attendu : "
           f"{TEMOIN_APPLICATIF.decode('ascii')!r}")

    lier_blocs(base)
    journal("T0 " + ("VERT" if not _echecs else f"échecs : {_echecs}"))

    # ---------------- T1 — LA RÉSOLUTION ----------------------------------------
    print("\nT1 — LA RÉSOLUTION (le VRAI ntdll lu par les DEUX lecteurs)")
    # L'ERRATUM n° 6 (le premier run du 06/11, 16:17 : le miroir Python
    # rendait -3 « répertoire export absent ») : les lecteurs de SSN
    # lisent LE VRAI ntdll — `ntdll_base`, JAMAIS `base` (l'artefact
    # cartographié : proxy.exe n'a PAS de répertoire export, le refus
    # était INÉVITABLE sur toute machine). Le CONTRÔLE PERMANENT vit à
    # l'assemblage : l'AST exige `ntdll_base` aux TROIS sites
    # (scripts/assembler_kit_m9f.py) — la faute ne peut plus dormir.
    try:
        ssn_create, stub_create = ssn_par_deux_lecteurs(
            ntdll_base, "NtCreateFile")
        ssn_ioctl, stub_ioctl = ssn_par_deux_lecteurs(
            ntdll_base, "NtDeviceIoControlFile")
        ssn_close, stub_close = ssn_par_deux_lecteurs(ntdll_base, "NtClose")
    except RuntimeError as e:
        journal(f"T1 : {e}")
        _echecs.append("T1.la-résolution")
        return _verdict()
    temoin(f"[T1] NtCreateFile          SSN {ssn_create} "
           f"(stub @{stub_create:#x}, motif {MOTIF_STUB.hex()})")
    temoin(f"[T1] NtDeviceIoControlFile SSN {ssn_ioctl} "
           "(jamais un numéro en cache : chaque geste résout)")
    temoin(f"[T1] NtClose               SSN {ssn_close}")
    journal("T1 VERT : les DEUX lecteurs d'accord sur les TROIS noms")

    # ---------------- T2 — L'ÉTABLISSEMENT --------------------------------------
    print("\nT2 — L'ÉTABLISSEMENT (le socket par le VRAI afd.sys)")

    def etablir(tag):
        """sys-04 : create + bind + connect, TROIS appels NT — le
        sockaddr DU KIT (family machine, port/adresse RÉSEAU)."""
        sockaddr = (struct.pack("<H", 2)              # AF_INET, boutisme
                    + struct.pack(">H", CIBLE_PORT)    # machine/réseau
                    + socket.inet_aton(ip_cible)       # la paire NOMMÉE
                    + b"\x00" * 8)                     # 16 o, la paire
        buf_sa = ctypes.create_string_buffer(sockaddr, 16)
        handle_sortie = ctypes.c_uint64(0)
        r = SYS04(ntdll_base, ctypes.cast(buf_sa, ctypes.c_void_p),
                  ctypes.cast(ctypes.byref(handle_sortie),
                              ctypes.c_void_p))
        verifie(f"{tag} : sys-04 (create + bind + connect, TROIS appels "
                "NT)", r == 0 and handle_sortie.value != 0,
                f"rax {r}, handle {handle_sortie.value:#x}")
        if r != 0:
            if r == -1:
                journal(f"{tag} : -1 une résolution a échoué (la cause vit "
                        "dans rdx au moment du verdict — l'information "
                        "existe, le kit la nomme par son étape)")
            elif r == -6:
                journal(f"{tag} : -6 un syscall a rendu un STATUS non nul "
                        "(le NTSTATUS vit dans rdx — AUCUN handle posé : "
                        "aucune possession partielle)")
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

    # ---------------- T3 — LA SESSION (OUVRIR) -----------------------------------
    print("\nT3 — LA SESSION (la poignée ENTIÈRE par le client de l'artefact)")

    alea = os.urandom(32)
    privee = os.urandom(32)
    temoin(f"[T3] l'aléa du kit        : {alea.hex()}")
    temoin(f"[T3] la clé privée du kit : {privee.hex()} (le clamp est le "
           "geste de tls13-14)")
    cle_publique_attendue = x25519_echelle(privee)
    temoin("[T3] la clé publique attendue (l'échelle RFC 7748 en "
           f"Python) : {cle_publique_attendue.hex()}")

    # le socle : DEUX rappels DU KIT, l'ABI msx64 de tls13-28 Q3
    journal_emissions = []

    def rappel_emission(ctx, ptr, n):
        journal_emissions.append(bytes(ctypes.string_at(ptr, n)))
        r = SYS05(ntdll_base, handle_1, ptr, n)
        if r != 0:
            journal(f"le rappel émission : sys-05 rend {r} (l'émission "
                    "TOTALE ou refusée — jamais un demi-envoi déguisé)")
        return r

    def rappel_reception(ctx, ptr, capacite):
        return SYS06(ntdll_base, handle_1, ptr, capacite)

    cb_emission = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                                   ctypes.c_void_p, ctypes.c_uint64)(
                                       rappel_emission)
    cb_reception = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                                    ctypes.c_void_p, ctypes.c_uint64)(
                                        rappel_reception)
    ctx_neutre = ctypes.c_uint64(0)       # les rappels ferment sur l'état
    socle = (ctypes.c_uint64 * 4)(
        ctypes.cast(cb_emission, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre),
        ctypes.cast(cb_reception, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre))

    session = ctypes.create_string_buffer(SESSION_TAILLE)
    kit96 = ctypes.create_string_buffer(KIT96)
    kit96.raw[:32] = alea
    kit96.raw[32:64] = privee
    kit96.raw[64:96] = EMPREINTE_EPINGLEE

    journal("T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états "
            "(le socle câblé aux SYSCALLS DIRECTS)")
    r = TLS27(ctypes.cast(session, ctypes.c_void_p), 1,
              ctypes.cast(socle, ctypes.c_void_p), KIT96)
    etat = struct.unpack_from("<I", session.raw, 1120)[0]
    verifie("T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ)",
            r == 0 and etat == 3, f"rax {r}, état {etat}")

    # LE RECOUP : l'offre émise == la construction re-jouée en Python
    ch_attendu = CH_RECORD + construction_ch_reference(alea,
                                                       cle_publique_attendue)
    ch_emis = journal_emissions[0] if journal_emissions else b""
    verifie("T3.recoup : le CH émis == 16 03 03 00 72 || la construction "
            "re-jouée (119 o)", ch_emis == ch_attendu,
            f"émis {len(ch_emis)} o — l'aléa du kit @ +6, la clé publique "
            "@ +82 == l'échelle Python : les DEUX lecteurs")
    if len(journal_emissions) >= 2:
        temoin(f"[T3] la dernière émission : {len(journal_emissions[-1])} "
               "o (le Finished client scellé sous NOS clés de poignée — "
               "le vol attendu : 58 o)")
    journal("T3 " + ("VERT" if not _echecs else f"échecs : {_echecs}"))
    if r != 0:
        if r == -6:
            journal("T3 : -6 L'ÉPINGLAGE DIVERGENT — le certificat servi "
                    "n'est plus celui de l'empreinte (un renouvellement "
                    "côté serveur ?) : renvoyez les pièces, le labo "
                    "re-gèle l'empreinte — c'est la nature de l'épinglage")
        elif r == -7:
            journal("T3 : -7 LE TRANSPORT EN ÉCHEC — le serveur n'a rien "
                    "servi après l'offre (réseau coupé ?) : réessayez "
                    "réseau vivant")
        elif r == -5:
            journal("T3 : -5 LA NÉGOCIATION REFUSÉE — le ServerHello a "
                    "choisi une autre suite (la cible a changé ?)")
        return _verdict()

    # ---------------- T4 — LA LIGNE APPLICATIVE ----------------------------------
    print("\nT4 — LA LIGNE (l'échange chiffré par LE CLIENT TLS 1.3 ENTIER)")
    ligne = ctypes.create_string_buffer(LIGNE_EMISE, len(LIGNE_EMISE))
    r = TLS27(ctypes.cast(session, ctypes.c_void_p), 2,
              ctypes.cast(ligne, ctypes.c_void_p), len(LIGNE_EMISE))
    verifie("T4.emettre : la ligne émise (rax == 0)", r == 0, f"rax {r}")
    if r != 0:
        return _verdict()

    tampon = ctypes.create_string_buffer(TAMPOIN_CAPACITE)
    flux_recu = b""
    temoin_trouve = False
    close_vu = False
    for i in range(64):
        r = TLS27(ctypes.cast(session, ctypes.c_void_p), 3,
                  ctypes.cast(tampon, ctypes.c_void_p), TAMPOIN_CAPACITE)
        if r < 0:
            if temoin_trouve:
                journal(f"T4 : le transport a rendu {r} APRÈS le témoin — "
                        "la ligne est ÉCHANGÉE, la fin est honnête")
                break
            journal(f"T4 : É3 rend {r} — la session est morte avant la "
                    "ligne (le verdict NOMMÉ de la machine)")
            break
        if r == 0:
            close_vu = True
            journal("T4 : le close_notify du serveur (l'état 4, la fin "
                    "PROPRE du protocole)")
            break
        flux_recu += tampon.raw[:r]
        if TEMOIN_APPLICATIF in flux_recu:
            temoin_trouve = True
            journal(f"T4 : le témoin « {TEMOIN_APPLICATIF.decode()} » REÇU "
                    f"et DÉCHIFFRÉ PAR LA MACHINE (record {i + 1}, "
                    f"{r} o restitués)")
            break
    verifie("T4.ligne : la ligne applicative chiffrée ÉCHANGÉE — le "
            "témoin dans le flux DÉCHIFFRÉ PAR LA MACHINE",
            temoin_trouve, f"{len(flux_recu)} o reconstitués, close_notify "
            f"{'oui' if close_vu else 'non'}")
    temoin(f"[T4] la tête du flux reçu : {flux_recu[:48].hex()}…")
    with open(os.path.join(PREUVES, "ligne-recue.txt"), "wb") as f:
        f.write(flux_recu[:65536])
    if not temoin_trouve:
        return _verdict()

    # ---------------- T5 — LA FALSIFICATION DE L'ÉPINGLAGE -----------------------
    print("\nT5 — LA FALSIFICATION (l'empreinte mutée contre LE VRAI serveur)")
    try:
        handle_2 = etablir("T5.session-2")
    except RefusNomme as e:
        journal(f"T5 : {e}")
        return _verdict()

    empreinte_mutee = bytearray(EMPREINTE_EPINGLEE)
    empreinte_mutee[3] ^= 1
    alea2 = os.urandom(32)
    privee2 = os.urandom(32)

    def rappel_emission_2(ctx, ptr, n):
        journal_emissions.append(bytes(ctypes.string_at(ptr, n)))
        return SYS05(ntdll_base, handle_2, ptr, n)

    def rappel_reception_2(ctx, ptr, capacite):
        return SYS06(ntdll_base, handle_2, ptr, capacite)

    cb_e2 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                             ctypes.c_void_p, ctypes.c_uint64)(
                                 rappel_emission_2)
    cb_r2 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                             ctypes.c_void_p, ctypes.c_uint64)(
                                 rappel_reception_2)
    socle2 = (ctypes.c_uint64 * 4)(
        ctypes.cast(cb_e2, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre),
        ctypes.cast(cb_r2, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre))
    session2 = ctypes.create_string_buffer(SESSION_TAILLE)
    kit96_2 = ctypes.create_string_buffer(KIT96)
    kit96_2.raw[:32] = alea2
    kit96_2.raw[32:64] = privee2
    kit96_2.raw[64:96] = bytes(empreinte_mutee)

    n_avant = len(journal_emissions)
    r = TLS27(ctypes.cast(session2, ctypes.c_void_p), 1,
              ctypes.cast(socle2, ctypes.c_void_p), KIT96)
    etat2 = struct.unpack_from("<I", session2.raw, 1120)[0]
    verifie("T5.falsification : -6 NOMMÉ (l'épinglage divergent), "
            "l'état 5", r == -6 and etat2 == 5, f"rax {r}, état {etat2}")
    verifie("T5.discipline : la session morte n'a émis QUE son offre",
            len(journal_emissions) - n_avant == 1,
            f"{len(journal_emissions) - n_avant} émission(s) après "
            "l'empreinte mutée")
    journal("T5 " + ("VERT : la garde constatée CONTRE LE VRAI SERVEUR — "
                     "la confiance est une comparaison, jamais une croyance"
                     if r == -6 else f"échec : rax {r}"))

    # ---------------- T6 — LA CLÔTURE --------------------------------------------
    print("\nT6 — LA CLÔTURE (le close_notify de la machine, NtClose par "
          "le trombone)")
    r = TLS27(ctypes.cast(session, ctypes.c_void_p), 4,
              ctypes.c_void_p(0), 0)
    etat = struct.unpack_from("<I", session.raw, 1120)[0]
    verifie("T6.fermer : le close_notify composé, scellé, ÉMIS (état 4)",
            r == 0 and etat == 4, f"rax {r}, état {etat}")
    if journal_emissions:
        dernier = journal_emissions[-1]
        verifie("T6.close_notify : la dernière émission == 24 o "
                "(5 + 2 + 17 : le scellé de 01 00)",
                len(dernier) == 24, f"{len(dernier)} o")

    # NtClose ÉMIS PAR SYS-01 : rax porte le SSN — ctypes ne peut pas le
    # charger ; un trampoline à DEUX instructions le fait (mov rax, ssn ;
    # jmp sys-01) — la fermeture est LE GESTE DU KIT (I8 de sys-04)
    trampoline_zone = k32.VirtualAlloc(None, 64, MEM_COMMIT,
                                       PAGE_EXECUTE_READWRITE)
    corps = (b"\x48\xb8" + struct.pack("<Q", ssn_close)
             + b"\xe9" + struct.pack("<i", (base + R_SYS01)
                                     - (trampoline_zone + 15)))
    ctypes.memmove(trampoline_zone, corps, len(corps))
    fermer = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(
        trampoline_zone)

    def fermer_handle(handle, tag):
        status = fermer(ctypes.c_void_p(handle))
        verifie(f"{tag} : NtClose émis par sys-01 (le trombone ABI)",
                status == 0, f"NTSTATUS {status & 0xffffffffffffffff:#x}")
        return status == 0

    fermer_handle(handle_1, "T6.session-1")
    fermer_handle(handle_2, "T6.session-2")
    k32.VirtualFree(trampoline_zone, 0, MEM_RELEASE)

    # l'intégrité : l'artefact relu inchangé, la cartographie libérée
    verifie("T6.intégrité : proxy.exe relu inchangé",
            sha256_fichier(chemin_proxy) == SHA_PROXY)
    with open(os.path.join(PREUVES, "journal-emissions.txt"), "wb") as f:
        f.write(b"".join(journal_emissions))
    temoin(f"[T6] les émissions du run : {len(journal_emissions)} "
           f"enregistrement(s), "
           f"{sum(len(e) for e in journal_emissions)} o")
    k32.FreeLibrary(base)
    journal("T6 " + ("VERT" if not _echecs else f"échecs : {_echecs}"))

    return _verdict()


def _verdict():
    lignes = []
    lignes.append("TRIADE — LE TERRAIN M9-(f) : LA SESSION RÉELLE")
    lignes.append("=" * 72)
    lignes.append(f"le run : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lignes.append("")
    if _echecs:
        lignes.append(f"VERDICT : ROUGE — {len(_echecs)} échec(s) nommé(s) :")
        for nom in _echecs:
            lignes.append(f"  - {nom}")
        lignes.append("")
        lignes.append("Un échec honnête vaut plus qu'un vert muet : la "
                      "ligne NOMME le défaut. Renvoyez preuves-m9f/ "
                      "TEL QUEL au coffre /test/preuves-m9f/.")
    else:
        lignes.append("VERDICT : VERT — LA SESSION RÉELLE ÉTABLIE :")
        lignes.append("  - le VRAI ntdll lu par sys-02 (les DEUX lecteurs "
                      "d'accord sur les TROIS SSN) ;")
        lignes.append("  - le socket par LE VRAI afd.sys (sys-04 : create + "
                      "bind + connect, TROIS appels NT, zéro ws2_32) ;")
        lignes.append("  - la poignée ENTIÈRE par LE CLIENT TLS 1.3 DE "
                      "L'ARTEFACT (le CH recoupé octet par octet contre "
                      "la construction re-jouée) ;")
        lignes.append("  - L'ÉPINGLAGE de l'empreinte attendue (la "
                      "falsification mutée → -6 NOMMÉ contre le serveur "
                      "réel) ;")
        lignes.append("  - LA LIGNE APPLICATIVE CHIFFRÉE ÉCHANGÉE (le "
                      "témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA "
                      "MACHINE) ;")
        lignes.append("  - le close_notify de la machine, NtClose par le "
                      "trombone sys-01.")
        lignes.append("")
        lignes.append("Renvoyez preuves-m9f/ EN ENTIER au coffre "
                      "/test/preuves-m9f/ — le laboratoire recoupe sur "
                      "pièces (D138/D145/D148) et, si elles établissent "
                      "le critère, la finale 1.0.0 est posée : le jalon "
                      "M9 franchi — LA GRANDE ŒUVRE.")
    lignes.append("")
    lignes.extend(_temoin)
    with open(os.path.join(PREUVES, "VERDICT-run-m9f.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    with open(os.path.join(PREUVES, "temoin-m9f.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(_temoin) + "\n")
    _ecrire_journal()
    print("\n" + "\n".join(lignes[:10]))
    print(f"\n[pièces] {PREUVES} — témoin, journal, verdict, ligne, émissions")
    return 1 if _echecs else 0


if __name__ == "__main__":
    sys.exit(main())
