#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reproduire_run_e3.py — reproduction labo du run e3 (D146).

Le proxy scellé 0.6.0-rc.1 (sha256 4b8f6af6…) ARMÉ --relever-https, émulé
FULL-PE sous unicorn (base préférée, IAT remplie par la marche des
descripteurs — modèle emulation_forensique.py D52h), rejouant LA SÉQUENCE
EXACTE du terrain e3 :

  1. ligne de commande : "C:\\kit\\proxy.exe" --relever-https
     (cmd /c mange les redirections — le proxy ne voit que ceci) ;
  2. connexion 1 (la sonde TCP du scénario) : connect puis FERMETURE
     immédiate — recv -> 0 octet ;
  3. connexion 2 (la sonde d'armement) : « GET http://127.0.0.1/ HTTP/1.1
     \\r\\nHost: 127.0.0.1\\r\\n\\r\\n » (43 o), puis fermeture.

Le binaire est LU, jamais écrit (frontière : le scellé ne bouge pas).
Sortie : le journal stdout capté (comparé au journal réel du run e3), les
octets envoyés au client (ce que page-sonde-armement.txt aurait dû porter),
la trace des API winsock/secur32, et LE DIAGNOSTIC si faute mémoire
(RIP traduit en bloc par le plan, désassemblage capstone, anneau des
dernières instructions).

Usage : python3 /home/z/my-project/scripts/reproduire_run_e3.py
"""

from __future__ import annotations

import importlib.util
import pathlib
import struct
import sys

import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_RIP,
                               UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10,
                               UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13,
                               UC_X86_REG_R14, UC_X86_REG_R15, UC_X86_REG_EFLAGS)
import capstone

REPO = pathlib.Path("/home/z/my-project/triade-repo")
EXE = REPO / "m5" / "proxy.exe"

# ---------------------------------------------------------------- plan PE
BASE = 0x140000000
TRAMP = 0x7FF700000000          # fausses API (une par import)
TRAMP_TAILLE = 0x10000
MAGIC_TRET = 0x7FF600000000     # retour d'un fil lancé par CreateThread
PILE = 0x7FF800000000           # piles (1 Mo par fil, pas de 0x100000)
PILE_TAILLE = 0x100000
SCRATCH = 0x7FF900000000        # cmdline UTF-16, addrinfo factices…
CMDLINE = SCRATCH + 0x1000
GAI_ZONE = SCRATCH + 0x4000

REQUETE_SONDE = (b"GET http://127.0.0.1/ HTTP/1.1\r\n"
                 b"Host: 127.0.0.1\r\n\r\n")
LIGNE_CMD = '"C:\\kit\\proxy.exe" --relever-https'

BUDGET_INSTRUCTIONS = 80_000_000

# ------------------------------------------------------------- blocs (plan)
def _charger(nom_fichier: str, nom: str):
    spec = importlib.util.spec_from_file_location(nom, REPO / nom_fichier)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def carte_blocs() -> list[tuple[int, int, str]]:
    blocs: list[tuple[int, int, str]] = []
    vus: set[tuple[int, int]] = set()
    for mod, cles in (("m1/layout.py", ("BLOCS_IO", "BLOCS_LIBC")),
                      ("m2/layout.py", ("BLOCS_IO", "BLOCS_TCP",
                                        "BLOCS_LIBC_EMBARQUES")),
                      ("m3/layout.py", ("BLOCS_IO", "BLOCS_M3",
                                        "BLOCS_TCP_EMBARQUES",
                                        "BLOCS_LIBC_EMBARQUES")),
                      ("m4/layout.py", ("BLOCS_REVISIONS", "BLOCS_TLS")),
                      ("m5/layout.py", ("BLOCS_REVISIONS_M5",))):
        try:
            M = _charger(mod, "lay_" + mod.replace("/", "_"))
        except Exception:
            continue
        for c in cles:
            for t in getattr(M, c, []) or []:
                # (id, nom, rva, taille, version, portee)
                rva, taille, nom_b = t[2], t[3], t[1]
                if (rva, taille) in vus:
                    continue
                vus.add((rva, taille))
                blocs.append((rva, taille, nom_b))
    blocs.sort()
    return blocs


BLOCS = carte_blocs()


def bloc_de(rva: int) -> str:
    prec = "?"
    for rva_b, taille, nom in BLOCS:
        if rva_b <= rva < rva_b + taille:
            return f"{nom} @0x{rva_b:X}+0x{rva - rva_b:X}"
        if rva_b > rva:
            return f"(après {prec}) 0x{rva:X}"
        prec = nom
    return f"(après {prec}) 0x{rva:X}"


# ---------------------------------------------------------------- l'image
data = EXE.read_bytes()
pe = pefile.PE(data=data)
assert pe.OPTIONAL_HEADER.ImageBase == BASE
T_IMAGE = pe.OPTIONAL_HEADER.SizeOfImage

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, ((T_IMAGE + 0xFFF) // 0x1000) * 0x1000)
uc.mem_write(BASE, data[:pe.OPTIONAL_HEADER.SizeOfHeaders])
for s in pe.sections:
    brut = s.get_data()
    tampon = bytearray(s.Misc_VirtualSize)
    tampon[:len(brut)] = brut
    uc.mem_write(BASE + s.VirtualAddress, bytes(tampon))

# ----------------------------------------------- IAT par marche descripteurs
imp_par_nom: dict[str, int] = {}     # "dll!Fonction" -> trampoline
tramp_suivant = {"i": 0}


def allouer_tramp(cle: str) -> int:
    if cle in imp_par_nom:
        return imp_par_nom[cle]
    t = TRAMP + tramp_suivant["i"] * 0x20
    tramp_suivant["i"] += 1
    imp_par_nom[cle] = t
    return t


for e in pe.DIRECTORY_ENTRY_IMPORT:
    dll = e.dll.decode().lower()
    for imp in e.imports:
        nom = (imp.name or b"?").decode()
        t = allouer_tramp(f"{dll}!{nom}")
        # le thunk par import (IAT réelle ou INT — les deux si distinctes)
        if imp.address:
            uc.mem_write(BASE + imp.address - BASE, struct.pack("<Q", t))
uc.mem_map(TRAMP, TRAMP_TAILLE)
uc.mem_map(MAGIC_TRET, 0x1000)
uc.mem_map(PILE, PILE_TAILLE * 8)
uc.mem_map(SCRATCH, 0x10000)

# la ligne de commande UTF-16 (ce que cmd /c transmet, redirections mangées)
uc.mem_write(CMDLINE, LIGNE_CMD.encode("utf-16-le") + b"\x00\x00")

# PREUVE CHIRURGICALE (--corrige) : la table des méthodes (R_TAB_METHODES
# 0x2410, héritage m4) stocke des RVA NUS (premier DWORD = RVA 32 bits,
# contrat du lecteur hérité http-02 @0x4D82 : « mov edx,[rax] ; add rdx,r12 »
# avec r12 = base d'image). La révision R3 de la ligne de flux lit le QWORD
# et le passe NU à la copie — l'ajout de base a été PERDU.
# En émulation SEULE (le binaire scellé sur disque ne bouge pas), on simule
# le correctif code-side AU CROCHET de l'appel .copier (0x850B) : rdx (le
# RVA nu) devient BASE + rdx, EXACTEMENT ce que ferait la notation corrigée.
# Si le crash disparaît et que la session repart jusqu'à connect, la cause
# est PROUVÉE chirurgicalement — le reste de l'exécution est code réel.
CORRIGE = "--corrige" in sys.argv
if CORRIGE:
    print("[preuve] correctif simulé au crochet 0x850B : "
          "rdx = BASE + rdx (idiome hérité http-02 restauré)")

# ------------------------------------------------------------ état du run
journal: list[bytes] = []            # stdout (WriteFile) — LE journal proxy
envois: dict[int, list[bytes]] = {}  # socket -> octets envoyés au client
appels: list[str] = []               # trace API (bornée en affichage)
anneau: list[int] = []               # dernières adresses exécutées
compteur = {"n": 0}
arret = {"code": None, "raison": ""}
fils: list[dict] = []                # fils lancés (start, param, ctx parent)

sockets: dict[int, dict] = {}        # id socket -> état scripté
soc_suivant = {"n": 0x500}


def nouvelle_socket(role: str) -> int:
    soc_suivant["n"] += 1
    s = soc_suivant["n"]
    sockets[s] = {"role": role, "recus": [], "ouvert": True}
    return s


# la séquence e3 : la sonde TCP (connexion morte) PUIS la sonde d'armement
SONDE_TCP = nouvelle_socket("sonde-tcp")
SONDE_ARMEMENT = nouvelle_socket("sonde-armement")
sockets[SONDE_TCP]["recus"] = [b""]                       # recv -> 0 : fermée
sockets[SONDE_ARMEMENT]["recus"] = [REQUETE_SONDE, b""]   # requête puis fermeture
accepts = [SONDE_TCP, SONDE_ARMEMENT]                    # la file d'accepts
ecoute = {"socket": None}


def c_chaine(addr: int, maxo: int = 256) -> str:
    if not addr:
        return "(null)"
    brut = uc.mem_read(addr, maxo)
    k = brut.find(b"\x00")
    if k >= 0:
        brut = brut[:k]
    return bytes(brut).decode("latin-1", "replace")


def c_chaine_l(arg: int) -> str:
    """PASCAL/UTF-16 : DWORD longueur puis octets larges (paquet tls-03)."""
    if not arg:
        return "(null)"
    n = struct.unpack("<I", uc.mem_read(arg, 4))[0]
    if n > 512:
        return f"(longueur folle {n})"
    brut = uc.mem_read(arg + 4, n * 2)
    return brut.decode("utf-16-le", "replace")


def r(nom_reg):
    return uc.reg_read(globals()[f"UC_X86_REG_{nom_reg}"])


def w(nom_reg, val):
    uc.reg_write(globals()[f"UC_X86_REG_{nom_reg}"], val)


REGS = ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
        "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "EFLAGS"]


def sauver_contexte() -> dict:
    return {k: r(k) for k in REGS} | {"RIP": r("RIP")}


def restaurer_contexte(ctx: dict) -> None:
    for k in REGS:
        w(k, ctx[k])
    w("RIP", ctx["RIP"])


# ------------------------------------------------------------- les API
def api_ret(valeur: int) -> None:
    w("RAX", valeur & 0xFFFFFFFFFFFFFFFF)
    w("RIP", struct.unpack("<Q", uc.mem_read(r("RSP"), 8))[0])
    w("RSP", r("RSP") + 8)


def ecrire_ptr(addr: int, valeur: int, taille: int = 8) -> None:
    if addr:
        uc.mem_write(addr, valeur.to_bytes(taille, "little"))


def api(nom: str) -> None:
    a1, a2, a3, a4 = r("RCX"), r("RDX"), r("R8"), r("R9")

    if nom == "kernel32!GetCommandLineW":
        appels.append("GetCommandLineW")
        api_ret(CMDLINE)

    elif nom == "kernel32!GetStdHandle":
        appels.append(f"GetStdHandle({a1})")
        api_ret(0xF00D0000 + (a1 & 0xF))

    elif nom == "kernel32!WriteFile":
        n = a3
        brut = bytes(uc.mem_read(a2, n)) if n else b""
        journal.append(brut)
        ecrire_ptr(a4, n)
        api_ret(1)

    elif nom == "kernel32!ReadFile":
        # le fil console : EOF (la lecture du run réel n'est pas jugée ici)
        appels.append(f"ReadFile(h=0x{a1:X}, buf=0x{a2:X}, n={a3:#x}, "
                      f"lu=0x{a4:X}) -> EOF")
        ecrire_ptr(a4, 0)
        api_ret(0)

    elif nom == "kernel32!ExitProcess":
        arret["code"] = a1
        arret["raison"] = "ExitProcess"
        appels.append(f"ExitProcess({a1})")
        uc.emu_stop()

    elif nom == "kernel32!CreateThread":
        start, param = a3, a4
        appels.append(f"CreateThread(start=0x{start:X}, param=0x{param:X})")
        # le contexte parent APRÈS le retour de CreateThread (jamais le
        # trampoline — sinon l'API se redéclenche à la restauration)
        ctx_parent = sauver_contexte()
        ret_addr = struct.unpack("<Q", uc.mem_read(ctx_parent["RSP"], 8))[0]
        ctx_parent["RSP"] += 8
        ctx_parent["RIP"] = ret_addr
        ctx_parent["RAX"] = 0x7E000000 + len(fils)   # handle factice
        fils.append({"start": start, "param": param, "ctx": ctx_parent})
        # fil AUJOURD'HUI : bas de pile neuf, MAGIC_TRET en retour
        pile_haut = PILE + (len(fils) + 1) * PILE_TAILLE
        w("RSP", pile_haut - 8)
        uc.mem_write(pile_haut - 8, struct.pack("<Q", MAGIC_TRET))
        w("RCX", param)
        w("RAX", 0)
        w("RIP", start)

    elif nom == "kernel32!CloseHandle":
        api_ret(1)

    elif nom == "kernel32!VirtualProtect":
        ecrire_ptr(a4, 0x40, 4)
        api_ret(1)

    elif nom in ("kernel32!InitializeCriticalSection",
                 "kernel32!EnterCriticalSection",
                 "kernel32!LeaveCriticalSection"):
        api_ret(0)

    elif nom == "ws2_32!WSAStartup":
        # WSADATA : version 2.2, le reste à zéro (408 o)
        uc.mem_write(a2, b"\x00" * 408)
        uc.mem_write(a2, struct.pack("<HH", 0x0202, 0x0202))
        appels.append("WSAStartup")
        api_ret(0)

    elif nom == "ws2_32!socket":
        s = nouvelle_socket(f"socket({a1},{a2},{a3})")
        if ecoute["socket"] is None and a2 == 1:
            ecoute["socket"] = s
        appels.append(f"socket({a1},{a2},{a3}) -> 0x{s:X}")
        api_ret(s)

    elif nom == "ws2_32!bind":
        appels.append(f"bind(0x{a1:X}, 0x{a2:X}, {a3})")
        api_ret(0)

    elif nom == "ws2_32!listen":
        appels.append(f"listen(0x{a1:X}, {a2})")
        api_ret(0)

    elif nom == "ws2_32!accept":
        if accepts:
            s = accepts.pop(0)
            appels.append(f"accept(0x{a1:X}) -> 0x{s:X} ({sockets[s]['role']})")
            api_ret(s)
        else:
            appels.append("accept(0x{a1:X}) -> INVALID (script épuisé)")
            api_ret(0xFFFFFFFFFFFFFFFF)

    elif nom == "ws2_32!recv":
        s = a1
        st = sockets.get(s)
        if st and st["recus"]:
            morceau = st["recus"].pop(0)
        else:
            morceau = b""
        if morceau:
            uc.mem_write(a2, morceau)
            appels.append(f"recv(0x{s:X}) -> {len(morceau)} o : "
                          f"{morceau[:48]!r}")
            api_ret(len(morceau))
        else:
            appels.append(f"recv(0x{s:X}) -> 0 (pair fermé)")
            api_ret(0)

    elif nom == "ws2_32!send":
        s, n = a1, a3
        brut = bytes(uc.mem_read(a2, n)) if n else b""
        envois.setdefault(s, []).append(brut)
        appels.append(f"send(0x{s:X}, {n} o) : {brut[:60]!r}")
        api_ret(n)

    elif nom == "ws2_32!closesocket":
        appels.append(f"closesocket(0x{a1:X})")
        if a1 in sockets:
            sockets[a1]["ouvert"] = False
        api_ret(0)

    elif nom == "ws2_32!WSAGetLastError":
        api_ret(0)

    elif nom == "ws2_32!WSACleanup":
        appels.append("WSACleanup")
        api_ret(0)

    elif nom == "ws2_32!getaddrinfo":
        noeud = c_chaine(a1) if a1 else "(null)"
        service = c_chaine(a2) if a2 else "(null)"
        appels.append(f"getaddrinfo(noeud={noeud!r}, service={service!r})")
        # une entrée : AF_INET / STREAM / TCP / 127.0.0.1:443
        z = GAI_ZONE
        sockaddr = struct.pack("<HH", 2, 0xBB01) + struct.pack(">I", 0x7F000001) + b"\x00" * 8
        ai = struct.pack("<IIIIQQQQ", 0, 2, 1, 6, 16, 0, z + 64, 0)
        uc.mem_write(z, ai)
        uc.mem_write(z + 64, sockaddr)
        ecrire_ptr(a4, z)
        api_ret(0)

    elif nom == "ws2_32!freeaddrinfo":
        appels.append("freeaddrinfo")
        api_ret(0)

    elif nom == "ws2_32!connect":
        fam, port = struct.unpack("<HH", uc.mem_read(a2, 4))
        addr = struct.unpack(">I", uc.mem_read(a2 + 4, 4))[0]
        appels.append(f"connect(0x{a1:X}) -> {addr}:{port >> 8}.{addr & 0xFF}"
                      f"{port & 0xFF} (fam={fam})")
        api_ret(0)

    elif nom.startswith("secur32!"):
        codes = {"AcquireCredentialsHandleW": 0, "FreeCredentialsHandle": 0,
                 "DeleteSecurityContext": 0}
        v = codes.get(nom.split("!")[1], 0x80090311)
        appels.append(f"{nom.split('!')[1]} -> 0x{v:X}")
        api_ret(v)

    else:
        appels.append(f"{nom} (non shimmé) -> 0")
        api_ret(0)


# ------------------------------------------------------------- les crochets
def crochet_code(uc_, adresse, taille, _):
    if adresse == MAGIC_TRET:
        return                       # emu_start(until) s'arrêtera dessus
    if CORRIGE and adresse == BASE + 0x850B:
        # correctif simulé : le RVA nu dans rdx devient VA complète
        rdx = r("RDX")
        if 0 < rdx < BASE:
            w("RDX", BASE + rdx)
    if TRAMP <= adresse < TRAMP + TRAMP_TAILLE:
        cle = [k for k, v in imp_par_nom.items() if v == adresse]
        if cle:
            nom_api = cle[0].replace(".dll!", "!")
            api(nom_api)
            return
    compteur["n"] += 1
    if compteur["n"] > BUDGET_INSTRUCTIONS:
        arret["raison"] = "budget d'instructions épuisé"
        uc_.emu_stop()
        return
    anneau.append(adresse)
    if len(anneau) > 48:
        anneau.pop(0)


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def crochet_faute(uc_, acces, adresse, taille, valeur, _):
    rip = r("RIP")
    rva = rip - BASE
    arret["raison"] = (f"FAUTE MÉMOIRE acces={acces} adresse=0x{adresse:X} "
                       f"taille={taille}")
    print("=" * 72)
    print(f"FAUTE MÉMOIRE — acces={acces} adresse=0x{adresse:X} "
          f"taille={taille} valeur=0x{valeur:X}")
    print(f"RIP = 0x{rip:X}  (RVA 0x{rva:X} — {bloc_de(rva)})")
    print("registres :")
    for k in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
              "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"):
        print(f"  {k:4s} = 0x{r(k):016X}")
    try:
        brut = bytes(uc.mem_read(rip, 16))
        for i in md.disasm(brut, rip):
            print(f"  faute sur : {i.mnemonic} {i.op_str}")
            break
    except Exception as exc:  # noqa: BLE001
        print(f"  (désassemblage impossible : {exc})")
    print("anneau (48 dernières adresses) :")
    for a in anneau:
        print(f"  0x{a:X}  RVA 0x{a - BASE:X}  {bloc_de(a - BASE)}")
    return False


uc.hook_add(UC_HOOK_CODE, crochet_code)
uc.hook_add(UC_HOOK_MEM_INVALID, crochet_faute)

# ------------------------------------------------------------------- GO
pile_haut = PILE + PILE_TAILLE          # le fil principal
uc.mem_write(pile_haut - 8, struct.pack("<Q", MAGIC_TRET))
w("RSP", pile_haut - 8)                 # entrée : rsp ≡ 8 (mod 16)
w("RCX", 0)
w("RDX", 0)
w("RIP", BASE + pe.OPTIONAL_HEADER.AddressOfEntryPoint)
contexte_principal = sauver_contexte()

import traceback  # noqa: E402

while True:
    try:
        uc.emu_start(r("RIP"), MAGIC_TRET)
    except Exception as exc:  # noqa: BLE001
        if not arret["raison"]:
            arret["raison"] = (f"exception émulation : "
                               f"{type(exc).__name__} : {exc}")
            traceback.print_exc()
        break
    if arret["raison"]:
        break
    if r("RIP") == MAGIC_TRET and fils:
        # le fil courant rend la main — restaurer le contexte de SON parent
        # (l'entrée poppée porte ce contexte, post-appel CreateThread)
        termine = fils.pop()
        restaurer_contexte(termine["ctx"])
        continue
    if r("RIP") == MAGIC_TRET:
        arret["raison"] = "le fil principal a rendu la main (fin naturelle)"
        break
    arret["raison"] = f"arrêt inexpliqué à RIP=0x{r('RIP'):X}"
    break

# -------------------------------------------------------------- le bilan
print("=" * 72)
print("BILAN DE LA REPRODUCTION E3")
print(f"raison de l'arrêt : {arret['raison'] or 'fin naturelle'}"
      + (f" — code {arret['code']}" if arret["code"] is not None else ""))
print(f"instructions exécutées : {compteur['n']}")
print("-" * 72)
print("JOURNAL STDOUT CAPTÉ (à comparer au proxy-journal.log réel) :")
for m in journal:
    for ligne in m.decode("latin-1").splitlines():
        print(f"  | {ligne}")
print("-" * 72)
print("OCTETS ENVOYÉS AU CLIENT (ce que page-sonde-armement aurait dû porter) :")
for s, morceaux in envois.items():
    for m in morceaux:
        print(f"  [socket 0x{s:X}] {len(m)} o : {m[:200]!r}")
if not envois:
    print("  (AUCUN — le client n'a rien reçu, comme au run réel)")
print("-" * 72)
print(f"TRACE API ({len(appels)} appels) :")
for a in appels:
    print(f"  {a}")
