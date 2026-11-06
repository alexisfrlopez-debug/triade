#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_specs_m9d.py — L'INSTRUMENT DE LA COUCHE I DU SOCLE SOCKET
(chantier M9-(d), phases 1+2 — l'ère 1.0.0 du transport, le geste miroir
de verifier_specs_m9a : le juge est le code).

Phase 1 (la couche I — R2 : l'écrit AVANT tout octet) : les specs, le
README § 9-14, le plan, les vecteurs dorés — 93 contrôles.
Phase 2 (LA NOTATION — l'écrit a précédé, la notation a suivi) : les
brouillons assemblés par l'auteur (keystone, rien d'autre), les mesures
676/289/287 o ARRÊTÉES D161-rejoué, la CONCORDANCE des constantes re-lues
de la notation contre le plan RE-DÉRIVÉ (jamais l'inverse), les citations
RIP des fixtures, la marche create→bind→connect dans les octets.

Ce que l'instrument juge (le plan M9-(d) : « le transport par SYSCALL
DIRECT, jamais l'IAT ws2_32, l'EAT de ntdll reste la source des SSN ») :

  C1  LES CONSTANTES RE-DÉRIVÉES PAR CODE — jamais une copie d'écriture :
      les QUATRE IOCTL par la macro canonique phnt (_AFD_CONTROL_CODE :
      FILE_DEVICE_NETWORK << 12 | Request << 2 | METHOD_NEITHER), recoupés
      aux VALEURS MESURÉES (leftarcode p.2/p.3/p.4 : 0x12003/0x12007/
      0x12017/0x1201F) ; les tailles des structures par struct.calcsize ;
      le C_ASSERT phnt (SEND == RECV) ; TDI_RECEIVE_NORMAL.

  C2  LES VECTEURS DORÉS — les dumps WinDbg Windows 11 (leftarcode,
      parties 1-4, juillet-août 2025) recopiés OCTET PAR OCTET : le EA de
      création (54 o), le bind IMPLICITE mswsock (20 o), le connect
      (40 o), le send (24 o) et le receive (24 o) — la notation les
      rejouera au harnais du geste suivant, le terrain les recoupera sur
      le VRAI afd.sys.

  C3  LA COUCHE I — les TROIS spécifications (sys-04 transport, sys-05
      émission, sys-06 réception) : le format du gabarit (Intention/
      Contrat/pre/post/inv), les constantes citées du PLAN (T5 : jamais
      recopiées), les frontières du socle tls13-28 (le zéro = -7, le
      partiel = -7), l'erratum de lecture AfdFlags/TdiFlags consigné à
      sys-06 AVANT la notation.

  C4  LE README RÉVISÉ — la charte du transport § 9-14, le tableau des
      TROIS specs, la provenance (phnt/ntafd.h + les mesures), la table
      des HUIT verdicts.

  C5  LE PLAN (m8/layout.py) — les slots PRÉFIGURÉS dans la réserve
      contiguë (0xA240-0xBFFF, multiples de 64, ordre croissant), les
      ANCIENS slots INTACTS (D161), les fixtures .text6 AU-DELÀ des
      fixtures poignée tls13 (concordance des DEUX plans), les noms NT
      aux longueurs exactes, la borne R_SYS_FIXTURES_FIN.

  C6  LES PIÈCES INTACTES — le scellé 0.9.0 relu (sha256 1492b0bc… de la
      carte génération 8), les notations sys-01..03 relues aux longueurs
      arrêtées, l'arbre tls13/I des 28 specs présent, les specs
      sys-01..03 inchangées.

  C7  R2 TENUE — AUCUN octet de notation sys-04/05/06 (ni notation
      explicite, ni brouillon) : la couche I précède, c'est la preuve
      même du geste.

Usage : python3 scripts/verifier_specs_m9d.py
Code de sortie : 0 = TOUT VERT, 1 = AU MOINS UN ÉCHEC (nommé).
"""

import hashlib
import importlib.util
import os
import pathlib
import re
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
VERTS, ECHECS = 0, []


def controle(nom, ok, detail=""):
    global VERTS
    if ok:
        VERTS += 1
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [ÉCHEC] {nom} — {detail}")


def section(titre):
    print(f"\n--- {titre}")


# ---------------------------------------------------------------------------
# (0) Les DEUX plans chargés par CHEMIN NOMINATIF (leçon D158 — jamais un
#     import anonyme : m4/layout.py est devant au sys.path des builders).
# ---------------------------------------------------------------------------

def _charger(nom, chemin):
    if nom in sys.modules:
        return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


section("(0) les DEUX plans par chemin nominatif")
L8 = _charger("layout_m8", REPO / "m8" / "layout.py")
L13 = _charger("layout_tls13", REPO / "tls13" / "layout.py")
controle("m8/layout.py ET tls13/layout.py chargés (la source unique + l'héritage)",
         True, f"IOCTL BIND={L8.IOCTL_AFD_BIND:#x}")

# ---------------------------------------------------------------------------
# (1) C1 — les constantes RE-DÉRIVÉES PAR CODE
# ---------------------------------------------------------------------------

section("(1) C1 — les constantes re-dérivées par code (le juge est le code)")


def _macro_afd(req, method=3):          # METHOD_NEITHER = 3 (phnt)
    return 0x12 << 12 | req << 2 | method  # FILE_DEVICE_NETWORK = 0x12


for nom, req, mes in (("BIND", 0, 0x12003), ("CONNECT", 1, 0x12007),
                      ("RECEIVE", 5, 0x12017), ("SEND", 7, 0x1201F)):
    controle(f"IOCTL_AFD_{nom} : macro({req}, NEITHER) == la mesure {mes:#x}",
            _macro_afd(req) == mes == getattr(L8, f"IOCTL_AFD_{nom}"),
            f"{_macro_afd(req):#x}")

controle("les REQ du plan == la table canonique phnt (BIND 0, CONNECT 1, RECV 5, SEND 7)",
         (L8.AFD_REQ_BIND, L8.AFD_REQ_CONNECT, L8.AFD_REQ_RECEIVE, L8.AFD_REQ_SEND)
         == (0, 1, 5, 7))

# les tailles structurelles par struct.calcsize (le petit boutisme x64)
controle("SOCKADDR 16 o (family u16 + port u16 + addr u32 + zero[8])",
         L8.SOCKADDR_TAILLE == struct.calcsize("<HHI8s") == 16)
controle("OBJECT_ATTRIBUTES 48 o (Length, RootDirectory, ObjectName, "
         "Attributes, SecurityDescriptor, SecurityQualityOfService)",
         L8.OBJECT_ATTRIBUTES_TAILLE == struct.calcsize("<IxxxxQQIxxxxQQ") == 0x30)
controle("l'UNICODE_STRING du device : Length 40 (20 UTF-16LE SANS NUL), "
         "MaximumLength 42 (AVEC) — l'ERRATUM corrigé sur pièces",
         len(L8.TXT_AFD_DEVICE) == L8.LEN_AFD_DEVICE == 40
         and len("\\Device\\Afd\\Endpoint".encode("utf-16le")) == 40
         and 40 + 2 == 42
         and "Length 40, MaximumLength 42" in
         (REPO / "m8" / "I" / "sys-04-transport.md").read_text(encoding="utf-8"))
controle("le WSABUF 12 o (len u32 + buf ptr 64 bits)",
         L8.WSABUF_TAILLE == struct.calcsize("<IQ") == 12)
controle("AFD_SEND_INFO == AFD_RECV_INFO : 24 o MESURÉS (l'IRP : "
         "InputBufferLength 0x18 ; 20 utiles par les champs + 4 de bourre "
         "terminal C — le C_ASSERT phnt)",
         L8.AFD_SENDRECV_TAILLE == 0x18
         == struct.calcsize("<QIII") + 4)
controle("l'IOSB 16 o (Status 8 + Information 8 — le compteur du transport)",
         L8.IOSB_TAILLE == struct.calcsize("<QQ") == 16)
controle("AFD_CONNECT 40 o == 24 de tête (0+0+0) + SOCKADDR 16",
         L8.AFD_CONNECT_TAILLE == 24 + L8.SOCKADDR_TAILLE == 0x28)
controle("AFD_BIND 20 o == flags u32 + SOCKADDR 16, la sortie 16 o (mesuré !irp)",
         L8.AFD_BIND_TAILLE == 4 + L8.SOCKADDR_TAILLE == 0x14
         and L8.AFD_BIND_SORTIE == 0x10)
controle("TDI_RECEIVE_NORMAL == 0x20 (la réception normale)",
         L8.TDI_RECEIVE_NORMAL == 0x20)
controle("AFD_WILDCARDADDRESS == 2 (le bind implicite : le noyau DÉDUIT)",
         L8.AFD_BIND_WILDCARD == 2)
controle("l'endpoint du jalon : AF_INET 2 · SOCK_STREAM 1 · IPPROTO_TCP 6",
         (L8.AF_INET, L8.SOCK_STREAM, L8.IPPROTO_TCP) == (2, 1, 6))
controle("le create : DesiredAccess 0xC0140000 mesuré, Options 0x20 SYNCHRONE, "
         "Disposition FILE_OPEN, ShareAccess RW, OBJ_CASE_INSENSITIVE 0x40",
         (L8.AFD_DESIRED_ACCESS, L8.AFD_CREATE_OPTIONS,
          L8.AFD_CREATE_DISPOSITION, L8.AFD_SHARE_ACCESS,
          L8.OBJ_CASE_INSENSITIVE) == (0xC0140000, 0x20, 1, 3, 0x40))
controle("la table des HUIT : le -7 TRANSPORT étend la table des SEPT",
         L8.V_TRANSPORT_ECHEC == -7 and L8.V_STATUS_NONNUL == -6
         and L8.V_RESOLU == 0 and L8.V_NOM_ABSENT == -1)
controle("le nom EA « AfdOpenPacketXX » : 15 o (phnt AfdOpenPacket == ReactOS "
         "AFD_PACKET_COMMAND_LENGTH)",
         L8.AFD_EA_NOM == b"AfdOpenPacketXX" and L8.LEN_AFD_EA_NOM == 15)
controle("EaValueLength 30 MESURÉ, le EA total 54 o (8 + 16 + 30)",
         L8.AFD_EA_VALEUR == 30 and L8.AFD_EA_TAILLE
         == 8 + L8.LEN_AFD_EA_NOM + 1 + L8.AFD_EA_VALEUR == 54)
controle("les noms NT : NtCreateFile 11 · NtDeviceIoControlFile 21 · NtClose 7 "
         "(des SPANS, jamais un NUL supposé)",
         (L8.LEN_NT_CREATEFILE, L8.LEN_NT_DEVICEIOCTL, L8.LEN_NT_CLOSE)
         == (11, 21, 7)
         and L8.TXT_NT_CREATEFILE == b"NtCreateFile"
         and L8.TXT_NT_DEVICEIOCTL == b"NtDeviceIoControlFile"
         and L8.TXT_NT_CLOSE == b"NtClose")

# ---------------------------------------------------------------------------
# (2) C2 — LES VECTEURS DORÉS (les mesures WinDbg Windows 11, leftarcode)
# ---------------------------------------------------------------------------

section("(2) C2 — les VECTEURS DORÉS (les dumps WinDbg Windows 11, recopiés)")

# p.1 : le dump du EA passé à NtCreateFile par ws2_32 (54 o d'EA, les 5
# derniers octets du dump original sont HORS EA — de la pile adjacente).
VECTEUR_EA_MESURE = bytes.fromhex(
    "00000000"                 # NextEntryOffset = 0
    "00"                       # Flags = 0
    "0F"                       # EaNameLength = 15
    "1E00"                     # EaValueLength = 30
    "4166644f70656e5061636b6574585800"      # « AfdOpenPacketXX\0 » (16 o)
    "00000000"                              # EndpointFlags = 0
    "00000000"                              # GroupID = 0
    "02000000"                              # AddressFamily = AF_INET
    "01000000"                              # SocketType = SOCK_STREAM
    "06000000"                              # Protocol = IPPROTO_TCP
    "00000000"                              # TransportDeviceNameLength = 0
    "0018BA5A4A33"                          # les 6 o résiduels de ws2_32 (bruit
                                            # de pile — afd.sys ne lit pas :
                                            # TDNL = 0)
)
NOTRE_EA = bytes.fromhex(
    "00000000" "00" "0F" "1E00"
    "4166644f70656e5061636b6574585800"
    "00000000" "00000000" "02000000" "01000000" "06000000" "00000000"
    "000000000000"                          # les NOTRES : NULS, déterministes
)
controle("le VECTEUR DORÉ EA : 54 o, EaNameLength 15, EaValueLength 30",
         len(VECTEUR_EA_MESURE) == 54 and VECTEUR_EA_MESURE[:8]
         == bytes.fromhex("00000000000F1E00")
         and VECTEUR_EA_MESURE[8:24] == b"AfdOpenPacketXX\x00")
controle("les 48 premiers octets du NOTRE EA == la mesure (l'en-tête + le nom "
         "+ les SIX DWORD utiles)",
         NOTRE_EA[:48] == VECTEUR_EA_MESURE[:48])
controle("la DIVERGENCE documentée : les 6 o de marge NULS chez nous, bruités "
         "chez ws2_32 (afd.sys ne lit pas au-delà : TDNL = 0) — le fixture "
         "est DÉTERMINISTE",
         NOTRE_EA[48:] == b"\x00" * 6 and len(NOTRE_EA) == 54)

# p.2 : le bind IMPLICITE mswsock au connect (TCPv4, 20 o)
VECTEUR_BIND = bytes.fromhex(
    "02000000"            # ShareAccess = AFD_WILDCARDADDRESS (le noyau DÉDUIT)
    "0200"                # AF_INET
    "0000"                # port 0 (le noyau choisira)
    "00000000"            # INADDR_ANY
    "FFFFFFFFFFFFFFFF"    # sin_zero : BRUIT résiduel mswsock (mesuré :
                          # « aucune signification », vérifié
                          # expérimentalement — p.2)
)
NOTRE_BIND = bytes.fromhex(
    "02000000" "0200" "0000" "00000000" "0000000000000000"
)
controle("le VECTEUR DORÉ bind : 20 o, flags WILDCARD 2, AF_INET, port 0, ANY",
         len(VECTEUR_BIND) == 20 and VECTEUR_BIND[:12]
         == bytes.fromhex("020000000200000000000000"))
controle("NOTRE fixture-bind == la mesure sur les 12 octets UTILES, sin_zero "
         "NUL (la divergence mesurée : le padding est SANS SIGNIFICATION)",
         NOTRE_BIND[:12] == VECTEUR_BIND[:12]
         and NOTRE_BIND[12:] == b"\x00" * 8 and len(NOTRE_BIND) == 20)

# p.2 : le connect (TCPv4 vers 192.168.1.1:80, 40 o)
VECTEUR_CONNECT = bytes.fromhex(
    "00" * 16 +                               # SanActive+pad, RootEndpoint=0
    "f019b5c85c020000"                         # ConnectEndpoint : LE HANDLE
                                               # (la MESURE : les zéros SONT
                                               # acceptés — p.2)
    "0200"                                     # AF_INET
    "0050"                                     # port 80 (BOUTISME RÉSEAU)
    "c0a80101"                                 # 192.168.1.1 (RÉSEAU)
    + "00" * 8                                 # sin_zero
)
controle("le VECTEUR DORÉ connect : 40 o, la tête de 16 o NULLE, le champ "
         "handle à +16, le sockaddr à +24 en BOUTISME RÉSEAU",
         len(VECTEUR_CONNECT) == 40
         and VECTEUR_CONNECT[:16] == b"\x00" * 16
         and VECTEUR_CONNECT[24:] == bytes.fromhex("02000050c0a80101"
                                                   "0000000000000000"))
controle("la MESURE des zéros acceptés : notre tête de 24 o NULLE "
         "(SanActive 0, Root 0, ConnectEndpoint 0)",
         24 + L8.SOCKADDR_TAILLE == L8.AFD_CONNECT_TAILLE)
controle("le sockaddr doré : family LE (0200), port BE (0050 = 80), "
         "adresse BE (c0a80101 = 192.168.1.1) — LE FORMAT, pas une conversion",
         bytes.fromhex("02000050c0a80101")[:2] == b"\x02\x00"
         and bytes.fromhex("02000050c0a80101")[2:4] == b"\x00\x50")

# p.3 : le send « AAAAAAAA » — AFD_SEND_INFO 24 o + WSABUF 12 o
VECTEUR_SEND_INFO = bytes.fromhex(
    "00000000c9532ff1"    # BufferArray (ptr mesuré — 0xc9532ff208 tronqué
                          # au petit boutisme du dump ; la VALEUR n'est pas
                          # dorée, LA STRUCTURE l'est)
    "01000000"            # BufferCount = 1
    "00000000"            # AfdFlags = 0 (la MESURE du send : aucun drapeau)
    "00000000"            # TdiFlags = 0
    "00000000"            # le bourre terminal C (l'IRP : InputBufferLength
                          # 0x18 = 24 — le sizeof aligné ptr)
)
VECTEUR_WSABUF = bytes.fromhex(
    "08000000"            # len = 8 (« AAAAAAAA »)
    "e0f22f53c9000000"    # buf (ptr mesuré)
)
controle("le VECTEUR DORÉ send : 24 o (ptr, 1, AfdFlags 0, TdiFlags 0) — "
         "la MESURE p.3",
         len(VECTEUR_SEND_INFO) == 24
         and VECTEUR_SEND_INFO[8:12] == bytes.fromhex("01000000")
         and VECTEUR_SEND_INFO[12:16] == b"\x00" * 4)
controle("le WSABUF doré : 12 o (len u32 = 8, buf ptr) — la charge pointée, "
         "AUCUNE copie",
         len(VECTEUR_WSABUF) == 12 and VECTEUR_WSABUF[:4]
         == bytes.fromhex("08000000"))

# p.4 : le receive — AFD_RECV_INFO 24 o, LE TROISIÈME champ = 0x20 (l'erratum)
VECTEUR_RECV_INFO = bytes.fromhex(
    "08e23aac01000000"    # BufferArray = 0x1ac3ae108... (ptr mesuré
                          # 0x1ac3ae108 — le dump dq ; la STRUCTURE est dorée)
    "01000000"            # BufferCount = 1
    "20000000"            # AfdFlags = 0x20 : TDI_RECEIVE_NORMAL — LA MESURE
                          # (« I have experimentally checked », p.4)
    "00000000"            # TdiFlags = 0
    "00000000"            # le bourre terminal (24 o mesurés)
)
controle("le VECTEUR DORÉ recv : 24 o, BufferCount 1, LE TROISIÈME champ "
         "(AfdFlags) = 0x20, TdiFlags = 0",
         len(VECTEUR_RECV_INFO) == 24
         and VECTEUR_RECV_INFO[12:16] == bytes.fromhex("20000000")
         and VECTEUR_RECV_INFO[16:20] == b"\x00" * 4)
controle("L'ERRATUM DE LECTURE (consigné à sys-06 AVANT la notation) : la "
         "MESURE met TDI_RECEIVE_NORMAL en champ AfdFlags (+12), la "
         "littérature le met en TdiFlags (+16) — la notation suivra la mesure",
         VECTEUR_RECV_INFO[12:16] == bytes.fromhex("20000000")
         and VECTEUR_RECV_INFO[16:20] == b"\x00" * 4
         and "ERRATUM DE LECTURE" in (REPO / "m8" / "I" / "sys-06-reception.md").read_text(encoding="utf-8"))
controle("la capacité dorée du recv : len = 0x1000 (4096, le code mesuré)",
         bytes.fromhex("00100000") == struct.pack("<I", 4096))

# ---------------------------------------------------------------------------
# (3) C3 — LA COUCHE I : les TROIS spécifications
# ---------------------------------------------------------------------------

section("(3) C3 — la couche I : les TROIS spécifications (R2 — l'écrit d'abord)")

SPECS = {
    "sys-04-transport": REPO / "m8" / "I" / "sys-04-transport.md",
    "sys-05-emission": REPO / "m8" / "I" / "sys-05-emission.md",
    "sys-06-reception": REPO / "m8" / "I" / "sys-06-reception.md",
}
textes = {}
for nom, chemin in SPECS.items():
    ok = chemin.exists()
    controle(f"{nom}.md existe (m8/I/)", ok)
    if ok:
        textes[nom] = chemin.read_text(encoding="utf-8")

def _a(nom, *morceaux):
    t = textes.get(nom, "")
    for m in morceaux:
        if m not in t:
            return False, m
    return True, ""


controle("le gabarit des TROIS : Intention/Contrat/pre/post/inv",
         all(all(m in textes.get(n, "") for m in
                 ("Intention :", "Contrat :", "pre  :", "post :", "inv  :"))
             for n in SPECS))
ok, manque = _a("sys-04-transport", "NtCreateFile", "\\Device\\Afd\\Endpoint",
                "AfdOpenPacketXX", "IOCTL_AFD_BIND", "IOCTL_AFD_CONNECT",
                "sys-02", "0xC0140000", "FILE_SYNCHRONOUS_IO_NONALERT",
                "WILDCARD", "le handle SYNCHRONE", "-1", "-6", "P3 r8",
                "le pointeur u64 de sortie du handle", "BOUTISME RÉSEAU",
                "TROIS", "résolutions", "NtDeviceIoControlFile")
controle("sys-04 : la séquence MESURÉE (create + bind WILDCARD + connect), "
         "les TROIS résolutions, le handle en [P3], -1/-6", ok, manque)
ok, manque = _a("sys-04-transport", "0x30", "OBJ_CASE_INSENSITIVE",
                "Length 40, MaximumLength 42", "54", "16 o", "40 o",
                "+24", "aucune possession "
                "partielle", "la fermeture n'est PAS un bloc")
controle("sys-04 : les tailles du plan citées (OA 0x30, UNICODE 42/44, EA 54, "
         "connect 40, sockaddr à +24) et la fermeture AU KIT", ok, manque)
ok, manque = _a("sys-05-emission", "IOCTL_AFD_SEND", "0x1201F", "WSABUF",
                "AUCUNE COPIE", "-7", "l'émission PARTIELLE", "TOTALE",
                "16406", "-5", "-6", "IOSB.Information", "AfdFlags = 0")
controle("sys-05 : TOTALE ou refus -7, aucune copie, les bornes, "
         "AfdFlags 0 mesuré", ok, manque)
ok, manque = _a("sys-06-reception", "IOCTL_AFD_RECEIVE", "0x12017",
                "TDI_RECEIVE_NORMAL", "0x20", "LA DEMI-FIN", "-7",
                "BLOQUANTE", "le tampon", "ERRATUM DE LECTURE", "AfdFlags",
                "le noyau écrit", "STATUS_CONNECTION_RESET")
controle("sys-06 : le recv bloquant, le zéro = -7 DEMI-FIN, l'erratum "
         "AfdFlags, le noyau ÉCRIT chez le kit", ok, manque)
controle("les TROIS specs citent sys-02 (le SSN résolu AU GESTE MÊME — "
         "la charte § 6)",
         all("sys-02" in textes[n] for n in SPECS))
controle("les TROIS specs : AUCUN IAT (la règle 3 TENUE pour le transport)",
         all("AUCUN IAT" in textes[n] for n in SPECS))
controle("les TROIS specs : le NOP 0x90 (la convention de la lignée)",
         all("NOP, 0x90" in textes[n] for n in SPECS))
controle("les TROIS specs portent la PROVENANCE (phnt + les mesures — "
         "l'écrit cite, le juge recoupe)",
         all(("leftarcode" in textes[n] or "diversenok" in textes[n]
              or "Hunt & Hackett" in textes[n] or "mesure" in textes[n].lower())
             for n in SPECS))
controle("les révisions : les TROIS à R1 (les identifiants stables)",
         all(textes[n].split("·")[0].strip().startswith("sys-0")
             and "révision 1" in textes[n].split("\n")[0] for n in SPECS))

# ---------------------------------------------------------------------------
# (4) C4 — le README révisé
# ---------------------------------------------------------------------------

section("(4) C4 — le README révisé : la charte § 9-14 et la provenance")
readme = (REPO / "m8" / "I" / "README.md").read_text(encoding="utf-8")
for morceau, nom in (
    ("Révision M9-(d)", "la section M9-(d)"),
    ("LE SOCLE SOCKET", "le titre du chantier"),
    ("§ 9", "la charte du transport"),
    ("Le sockaddr est une DONNÉE du kit", "la règle 9"),
    ("L'émission est TOTALE ou refusée", "la règle 10"),
    ("le zéro est LA DEMI-FIN", "la règle 11"),
    ("La fermeture est AU KIT", "la règle 14"),
    ("sys-04:R1", "le tableau des specs"),
    ("g90004", "les blocs machine"),
    ("phnt/ntafd.h", "la provenance canonique"),
    ("leftarcode.com", "la provenance des mesures"),
    ("WinDbg", "les mesures Windows 11"),
    ("HUIT", "la table des HUIT verdicts"),
    ("-7", "le verdict transport"),
    ("R2 tenue", "l'écrit-avant-code"),
    ("AUCUN octet de notation", "la preuve R2"),
    ("0x10C20", "les fixtures .text6"),
    ("ÉPUISÉE par K[64]", "la réserve .rdata M8 honorée"),
):
    controle(f"le README porte {nom}", morceau in readme)
controle("la charte d'origine INTACTE : les § 1-8 toujours là (la révision "
         "AJOUTE, elle ne réécrit pas)",
         all(m in readme for m in ("SSN est une DONNÉE", "MOTIF_STUB",
                                   "Aucun IAT", "Fail-closed intégral",
                                   "Zéro état détenu", "réserve d'ère")))

# ---------------------------------------------------------------------------
# (5) C5 — le plan : les slots, les fixtures, les bornes
# ---------------------------------------------------------------------------

section("(5) C5 — le plan : les slots préfigurés, les fixtures, les bornes")
reserve = L8.ZONE_SYS_RESERVE
controle("la réserve contiguë .text5 : 0xA240-0xBFFF (la croissance nommée M8)",
         reserve == (0xA240, 0xBFFF))
controle("les ANCIENS slots INTACTS : g90001-3 aux ARRÊTS D161 "
         "(0xA000/0x40, 0xA040/0x140, 0xA180/0xC0)",
         tuple(L8.SLOTS_SYS[b] for b in ("g90001", "g90002", "g90003"))
         == ((0xA000, 0x40), (0xA040, 0x140), (0xA180, 0xC0)))
controle("les slots préfigurés DANS la réserve, multiples de 64, ordre "
         "croissant strict, sous la borne",
         all(reserve[0] <= va and (va % 64 == 0) and (taille % 64 == 0)
             for va, taille in (L8.SLOTS_SYS["g90004"],
                                L8.SLOTS_SYS["g90005"],
                                L8.SLOTS_SYS["g90006"]))
         and L8.SYS04_VA < L8.SYS05_VA < L8.SYS06_VA
         and L8.SYS06_VA + L8.SLOTS_SYS["g90006"][1] - 1 <= reserve[1])
controle("L'ARRÊT D161 REJOUÉ au geste de la notation : les mesures "
         "676/289/287 o consignées au plan (la préfiguration s'est inclinée)",
         "676 o MESURÉS" in (REPO / "m8" / "layout.py").read_text(encoding="utf-8")
         and "289 o MESURÉS" in (REPO / "m8" / "layout.py").read_text(encoding="utf-8")
         and "287 o MESURÉS" in (REPO / "m8" / "layout.py").read_text(encoding="utf-8"))
controle("les NOMS_BLOCS étendus : g90004/05/06 aux noms des specs",
         tuple(L8.NOMS_BLOCS[b] for b in ("g90004", "g90005", "g90006"))
         == ("sys-04-transport", "sys-05-emission", "sys-06-reception"))
controle("les NOMS_BLOCS d'origine INTACTS (g90001-3)",
         tuple(L8.NOMS_BLOCS[b] for b in ("g90001", "g90002", "g90003"))
         == ("sys-01-emetteur", "sys-02-resolveur", "sys-03-ecriture"))

# la concordance des DEUX plans : les fixtures sys AU-DELÀ des fixtures
# poignée tls13 (fin R_HRR + 32), alignés 16, sous la borne R_SYS_FIXTURES_FIN
fin_tls13 = L13.R_HRR + 32
controle("la fin des fixtures poignée tls13 : R_HRR 0x10BF0 + 32 = 0x10C10",
         fin_tls13 == 0x10C10)
controle("les fixtures sys AU-DELÀ de la fin tls13 (AUCUN chevauchement — "
         "l'ARRÊT D95 honoré)",
         L8.R_SYS_DEVICE >= fin_tls13
         and all(va >= fin_tls13 for va in (L8.R_SYS_EA, L8.R_SYS_BIND,
                                            L8.R_SYS_NOM_CREATEFILE,
                                            L8.R_SYS_NOM_DEVICEIOCTL,
                                            L8.R_SYS_NOM_CLOSE)))
controle("les fixtures sys alignés 16 et ordonnés",
         all(va % 16 == 0 for va in (L8.R_SYS_DEVICE, L8.R_SYS_EA,
                                     L8.R_SYS_BIND, L8.R_SYS_NOM_CREATEFILE,
                                     L8.R_SYS_NOM_DEVICEIOCTL,
                                     L8.R_SYS_NOM_CLOSE))
         and L8.R_SYS_DEVICE < L8.R_SYS_EA < L8.R_SYS_BIND
         < L8.R_SYS_NOM_CREATEFILE < L8.R_SYS_NOM_DEVICEIOCTL
         < L8.R_SYS_NOM_CLOSE < L8.R_SYS_FIXTURES_FIN)
controle("chaque fixture dans son logement : device 42 ≤ 48, EA 54 ≤ 64, "
         "bind 20 ≤ 32, les noms ≤ leurs espaces (alignés 16 consécutifs)",
         (L8.R_SYS_EA - L8.R_SYS_DEVICE) >= 42
         and (L8.R_SYS_BIND - L8.R_SYS_EA) >= 54
         and (L8.R_SYS_NOM_CREATEFILE - L8.R_SYS_BIND) >= 20
         and (L8.R_SYS_NOM_DEVICEIOCTL - L8.R_SYS_NOM_CREATEFILE) >= 11
         and (L8.R_SYS_NOM_CLOSE - L8.R_SYS_NOM_DEVICEIOCTL) >= 21
         and (L8.R_SYS_FIXTURES_FIN - L8.R_SYS_NOM_CLOSE) >= 7)
controle("la borne R_SYS_FIXTURES_FIN : le prochain fixture pose ICI, "
         "jamais au-delà sans arrêt nommé (miroir D95)",
         L8.R_SYS_FIXTURES_FIN == 0x10CF0)
controle("l'ancien fixture R_SYS_NOM (NtWriteFile, 0x2EC0) INTACT — "
         "la réserve .rdata d'origine ne bouge pas",
         L8.R_SYS_NOM == 0x2EC0 and L8.R_SYS_LIGNE == 0x2ED0)

# ---------------------------------------------------------------------------
# (6) C6 — les pièces intactes
# ---------------------------------------------------------------------------

section("(6) C6 — les pièces intactes (le scellé, les notations, l'arbre M9)")

sha = hashlib.sha256((REPO / "m8" / "proxy.exe").read_bytes()).hexdigest()
controle("le scellé 0.9.0 relu : m8/proxy.exe sha256 1492b0bc… (la carte "
         "génération 8, R7)",
         sha == "1492b0bc0792e1ab162338b414fb20573134e84d"
                "752b9d0657292421f8eb0cd4", sha[:16] + "…")

for nom, taille_mesuree in (("sys-01-emetteur", 6), ("sys-02-resolveur", 293),
                            ("sys-03-ecriture", 164)):
    chemin = REPO / "m8" / "notation" / f"{nom}.asm"
    ok = chemin.exists() and f"Code : {taille_mesuree} o" \
        in chemin.read_text(encoding="utf-8")
    controle(f"la notation {nom}.asm relue : la longueur arrêtée "
             f"{taille_mesuree} o citée en tête", ok,
             f"la mesure D161 : {taille_mesuree} o")

for nom, bid in (("sys-04-transport", "g90004"),
                 ("sys-05-emission", "g90005"),
                 ("sys-06-reception", "g90006")):
    chemin = REPO / "m8" / "notation" / f"{nom}.asm"
    texte = chemin.read_text(encoding="utf-8") if chemin.exists() else ""
    m = re.search(r"Code : (\d+) o · padding : (\d+) o", texte)
    code, padding = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    va, slot = L8.SLOTS_SYS[bid]
    controle(f"la notation {nom}.asm relue : le code {code} o + padding "
             f"{padding} o == le slot {slot:#x} ARRÊTÉ", code + padding == slot
             and padding >= 16, f"676/289/287 o MESURÉS — la préfig s'est inclinée")

controle("les brouillons sys-01..03 présents (l'outillage auteur intact)",
         all((REPO / "m8" / "notation" / "brouillons" / f"{n}.asm").exists()
             for n in ("sys-01-emetteur", "sys-02-resolveur",
                       "sys-03-ecriture")))

controle("l'arbre tls13/I des 28 specs présent (l'arbre M9 INTACT — "
         "verifier_specs_m9a en est le juge dédié)",
         len(list((REPO / "tls13" / "I").glob("tls13-*.md"))) == 28)
controle("les specs sys-01..03 INCHANGÉES (présentes, le format tenu)",
         all((REPO / "m8" / "I" / f"sys-0{i}-{r}.md").exists()
             for i, r in ((1, "emetteur"), (2, "resolveur"), (3, "ecriture"))))
controle("l'ancien LISEZMOI m8d présent (le kit terrain M8-(d) intact)",
         (REPO / "m8" / "terrain" / "LISEZMOI-m8d.txt").exists())

# ---------------------------------------------------------------------------
# (7) C7 — LA NOTATION PRÉSENTE + CONCORDANTE (la R2 a vécu : l'écrit a
# précédé, la notation a suivi — le juge re-dérive les constantes de la
# notation CONTRE le plan, jamais l'inverse)
# ---------------------------------------------------------------------------

section("(7) C7 — la notation du socle présente + concordante au plan")

# la concordance : chaque constante du transport RE-LUE de la notation et
# RE-DÉRIVÉE du plan (le juge est le code — la notation cite, l'instrument
# recoupe : les IOCTL par la macro canonique, les tailles par struct, les
# drapeaux par leurs valeurs)
notation_04 = (REPO / "m8" / "notation" / "sys-04-transport.asm").read_text(
    encoding="utf-8").lower()
notation_05 = (REPO / "m8" / "notation" / "sys-05-emission.asm").read_text(
    encoding="utf-8").lower()
notation_06 = (REPO / "m8" / "notation" / "sys-06-reception.asm").read_text(
    encoding="utf-8").lower()

for morceau, nom in (
    (f"mov edx, {L8.AFD_DESIRED_ACCESS:#x}", "DesiredAccess (ZÉRO-étendu — "
     "la leçon du round-trip : mov edx, JAMAIS mov rdx dont le C7 signerait)"),
    (f"mov dword ptr [rsp + 0x90], {L8.OBJECT_ATTRIBUTES_TAILLE:#x}",
     "OBJECT_ATTRIBUTES.Length 0x30"),
    (f"mov dword ptr [rsp + 0xa8], {L8.OBJ_CASE_INSENSITIVE:#x}",
     "OBJ_CASE_INSENSITIVE 0x40"),
    (f"mov word ptr [rsp + 0xc0], {L8.LEN_AFD_DEVICE}",
     "UNICODE_STRING.Length 40 SANS le NUL (l'erratum de l'instrument)"),
    (f"mov word ptr [rsp + 0xc2], {L8.LEN_AFD_DEVICE + 2}",
     "UNICODE_STRING.MaximumLength 42 AVEC"),
    (f"mov qword ptr [rsp + 0x50], {L8.AFD_EA_TAILLE}", "EaLength 54"),
    (f"mov qword ptr [rsp + 0x28], {L8.IOCTL_AFD_BIND:#x}", "IOCTL_AFD_BIND"),
    (f"mov qword ptr [rsp + 0x38], {L8.AFD_BIND_TAILLE:#x}",
     "AFD_BIND_TAILLE 0x14"),
    (f"mov qword ptr [rsp + 0x48], {L8.AFD_BIND_SORTIE:#x}",
     "AFD_BIND_SORTIE 0x10"),
    (f"mov qword ptr [rsp + 0x28], {L8.IOCTL_AFD_CONNECT:#x}",
     "IOCTL_AFD_CONNECT"),
    (f"mov qword ptr [rsp + 0x38], {L8.AFD_CONNECT_TAILLE:#x}",
     "AFD_CONNECT_TAILLE 0x28"),
    (f"mov edx, {L8.LEN_NT_CREATEFILE}", "« NtCreateFile » 11 o"),
    (f"mov edx, {L8.LEN_NT_DEVICEIOCTL}", "« NtDeviceIoControlFile » 21 o"),
):
    controle(f"sys-04 concorde : {nom}", morceau in notation_04)

for morceau, nom in (
    (f"mov qword ptr [rsp + 0x28], {L8.IOCTL_AFD_SEND:#x}", "IOCTL_AFD_SEND"),
    (f"mov qword ptr [rsp + 0x38], {L8.AFD_SENDRECV_TAILLE:#x}",
     "AFD_SEND_INFO 0x18 (le C_ASSERT send == recv)"),
    ("mov dword ptr [rsp + 0x78], 1", "BufferCount 1"),
    ("mov dword ptr [rsp + 0x7c], 0", "AfdFlags 0 (la MESURE p.3)"),
    ("mov dword ptr [rsp + 0x80], 0", "TdiFlags 0"),
):
    controle(f"sys-05 concorde : {nom}", morceau in notation_05)

for morceau, nom in (
    (f"mov qword ptr [rsp + 0x28], {L8.IOCTL_AFD_RECEIVE:#x}",
     "IOCTL_AFD_RECEIVE"),
    (f"mov dword ptr [rsp + 0x7c], {L8.TDI_RECEIVE_NORMAL:#x}",
     "AfdFlags = TDI_RECEIVE_NORMAL 0x20 — L'ERRATUM TENU (LA MESURE en "
     "TROISIÈME champ, la littérature serait refusée par le noyau strict)"),
    ("mov dword ptr [rsp + 0x80], 0", "TdiFlags 0 (RIEN ici : la "
     "littérature faussière serait refusée)"),
):
    controle(f"sys-06 concorde : {nom}", morceau in notation_06)

# les citations RIP : les fixtures CITÉS par déplacement, les cibles
# re-lues des en-têtes et re-contrôlées contre le plan
def _cibles_rip(nom_fichier):
    brut = (REPO / "m8" / "notation" / f"{nom_fichier}.asm").read_text(
        encoding="utf-8")
    deplacements = re.findall(
        r";\s+0x([0-9a-f]+) \+ 0x([0-9a-f]+) ([+-]) 0x([0-9a-f]+) = 0x([0-9a-f]+)",
        brut)
    cibles = []
    for adr, t, signe, disp, cible in deplacements:
        calc = (int(adr, 16) + int(t, 16)
                + (int(disp, 16) if signe == "+" else -int(disp, 16)))
        assert calc == int(cible, 16), f"arithmétique RIP fausse @ {adr}"
        cibles.append(calc)
    return cibles


controle("sys-04 : les SIX déplacements RIP citent EXACTEMENT les fixtures "
         "du plan (device, EA, bind, les DEUX noms)",
         sorted(_cibles_rip("sys-04-transport"))
         == sorted([L8.R_SYS_DEVICE, L8.R_SYS_EA, L8.R_SYS_BIND,
                    L8.R_SYS_NOM_CREATEFILE, L8.R_SYS_NOM_DEVICEIOCTL,
                    L8.R_SYS_NOM_DEVICEIOCTL]))
controle("sys-05/sys-06 : l'unique déplacement RIP cite le nom de résolution",
         _cibles_rip("sys-05-emission") == [L8.R_SYS_NOM_DEVICEIOCTL]
         and _cibles_rip("sys-06-reception") == [L8.R_SYS_NOM_DEVICEIOCTL])

# la marche : create PUIS bind PUIS connect — les alternances dans les octets
controle("sys-04 : l'alternance résoudre-émettre × 3 (la séquence MESURÉE "
         "mswsock, I6/Q3 — chaque geste résout)",
         re.findall(rf"call ({L8.SYS02_VA:#x}|{L8.SYS01_VA:#x})", notation_04)
         == [f"{L8.SYS02_VA:#x}", f"{L8.SYS01_VA:#x}"] * 3)
controle("sys-05/sys-06 : résoudre PUIS émettre (I3)",
         notation_05.find(f"call {L8.SYS02_VA:#x}")
         < notation_05.find(f"call {L8.SYS01_VA:#x}")
         and notation_06.find(f"call {L8.SYS02_VA:#x}")
         < notation_06.find(f"call {L8.SYS01_VA:#x}"))

# les brouillons présents (l'outillage auteur : keystone assemble, rien
# d'autre — les notations explicites en dérivent)
controle("les brouillons sys-04..06 présents (l'outillage auteur intact)",
         all((REPO / "m8" / "notation" / "brouillons" / f"{n}.asm").exists()
             for n in ("sys-04-transport", "sys-05-emission",
                       "sys-06-reception")))

# ---------------------------------------------------------------------------
# BILAN
# ---------------------------------------------------------------------------

print("\n" + "=" * 70)
total = VERTS + len(ECHECS)
print(f"BILAN : {total} contrôles · {VERTS} verts · "
      f"{len(ECHECS)} échec(s)")
if ECHECS:
    print("ÉCHECS NOMMÉS : " + ", ".join(ECHECS))
print("=" * 70)
sys.exit(1 if ECHECS else 0)
