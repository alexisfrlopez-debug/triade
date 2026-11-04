#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_base_reelle.py — contrôle d'exécution full-PE À LA BASE RÉELLE
(D146 — livrable du jalon M5, rejouable par script).

LA RÈGLE (D146, Entrée 141) : « AUCUN scellage rc/final sans un contrôle
d'exécution full-PE à la base réelle de l'image. L'émulation à base 0 n'est
pas un témoin de l'exécution réelle — un RVA nu y résout par accident. Le
contrôle exécute une requête routée SERVIE (ou nomme le crash) avant que la
carte ne se scelle. »

L'ANGLE MORT COUVERT : les oracles différentiels jugent la LOGIQUE (à base 0,
RVA = adresse : le défaut du rc.1 y était invisible PAR PRINCIPE) ; la
conformité § 8.2 lit le PE sans l'exécuter. Ce contrôle est le TÉMOIN de
l'adressage RÉEL de l'image chargée.

LE MOTEUR (modèle emulation_forensique D52h, éprouvé par le diagnostic du
run e3 — scripts/reproduire_run_e3.py) :
  - l'image PE ENTIÈRE est chargée à sa base préférée (0x140000000) ;
  - l'IAT est remplie par la MARCHE des descripteurs d'import (ce que fait
    le chargeur Windows — motif D54) ;
  - la ligne de commande RÉELLE est passée (GetCommandLineW shimmé) ;
  - les fils sont coopératifs (CreateThread shimmé, contexte parent
    sauvegardé — la boucle accept et les sessions vivent en parallèle) ;
  - les API winsock/secur32 sont scriptées (shims — le contrôle constate
    l'adressage et le chemin de session, PAS la vraie Schannel, frontière
    D146).

LA SÉQUENCE (le terrain e3 rejoué — les deux connexions du scénario) :
  1. « <proxy> --relever-https » (l'armement, http-12:R3) ;
  2. connexion 1 : la sonde TCP morte (recv -> 0, fermeture immédiate) ;
  3. connexion 2 : la sonde d'armement — « GET http://127.0.0.1/ HTTP/1.1
     Host: 127.0.0.1 » en forme ABSOLUE : la requête est PARSÉE puis ROUTÉE
     (politique armée : relèvement http->https amont) — ELLE traverse la
     session http-10:R3, écrit LA LIGNE DE FLUX (la méthode lue de
     R_TAB_METHODES à la base réelle — LE point du correctif rc.2, l'idiome
     hérité http-02:R1 restauré) et reçoit une RÉPONSE (le refus nommé du
     contrat sur poignée shimmée défaillante — SEC_E_NO_AUTHENTICATING_
     AUTHORITY, frontière assumée).

LE VERDICT :
  VERT ssi (a) AUCUNE faute mémoire (sinon : NOMMÉE — adresse, instruction,
  bloc, anneau des 48 dernières adresses) ; (b) la ligne de flux est ÉMISE
  dans le journal avec la MÉTHODE EN TEXTE (« flux GET … » — un pointeur RVA
  nu y crashe, c'est la leçon du rc.1) ; (c) le CLIENT A REÇU des octets
  sur la socket routée (réponse ou refus nommé du contrat).
  Toute divergence est NOMMÉE (fail-closed) : le contrôle ne peut pas
  « passer » en silence.

Usage :  python3 m5/controle_base_reelle.py [--chemin m5/proxy.exe]
Intégré au scellage (build_m5._sceller) : VERT exigé AVANT la bascule de
balise rc/final — D146, « avant que la carte ne se scelle ».
Code de sortie : 0 = VERT, 1 = KO (pièces nommées), 2 = erreur fatale.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
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
                               UC_X86_REG_R14, UC_X86_REG_R15)
import capstone

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent

# ---------------------------------------------------------------- plan PE
BASE = 0x140000000                # la base préférée de l'image (D146)
TRAMP = 0x7FF700000000            # fausses API (une par import)
TRAMP_TAILLE = 0x10000
MAGIC_TRET = 0x7FF600000000       # retour d'un fil lancé par CreateThread
PILE = 0x7FF800000000             # piles (1 Mo par fil, pas de 0x100000)
PILE_TAILLE = 0x100000
SCRATCH = 0x7FF900000000          # cmdline UTF-16, addrinfo factices…
CMDLINE = SCRATCH + 0x1000
GAI_ZONE = SCRATCH + 0x4000

REQUETE_SONDE = (b"GET http://127.0.0.1/ HTTP/1.1\r\n"
                 b"Host: 127.0.0.1\r\n\r\n")
LIGNE_CMD = '"C:\\kit\\proxy.exe" --relever-https'

BUDGET_INSTRUCTIONS = 120_000_000

REGS = ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
        "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"]

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


# ---------------------------------------------------------------- le moteur
class ControleBaseReelle:
    """Une exécution full-PE à la base réelle — la séquence e3 rejouée."""

    def __init__(self, chemin_exe: pathlib.Path):
        self.chemin = chemin_exe
        self.journal: list[bytes] = []            # stdout (WriteFile)
        self.envois: dict[int, list[bytes]] = {}  # socket -> octets au client
        self.appels: list[str] = []               # trace API (bornée)
        self.anneau: list[int] = []               # dernières adresses
        self.compteur = {"n": 0}
        self.arret: dict = {"code": None, "raison": ""}
        self.fils: list[dict] = []
        self.sockets: dict[int, dict] = {}
        self.soc_suivant = {"n": 0x500}
        self.imp_par_nom: dict[str, int] = {}
        self.tramp_suivant = {"i": 0}
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self._preparer()

    # ------------------------------------------------------------- l'image
    def _preparer(self) -> None:
        data = self.chemin.read_bytes()
        self.pe = pe = pefile.PE(data=data)
        if pe.OPTIONAL_HEADER.ImageBase != BASE:
            raise RuntimeError(f"base préférée inattendue : "
                               f"{pe.OPTIONAL_HEADER.ImageBase:#x} != {BASE:#x}")
        self.data = data
        t_image = pe.OPTIONAL_HEADER.SizeOfImage
        uc = self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc.mem_map(BASE, ((t_image + 0xFFF) // 0x1000) * 0x1000)
        uc.mem_write(BASE, data[:pe.OPTIONAL_HEADER.SizeOfHeaders])
        for s in pe.sections:
            brut = s.get_data()
            tampon = bytearray(s.Misc_VirtualSize)
            tampon[:len(brut)] = brut
            uc.mem_write(BASE + s.VirtualAddress, bytes(tampon))

        # IAT par marche des descripteurs (le chargeur réel, motif D54)
        for e in pe.DIRECTORY_ENTRY_IMPORT:
            dll = e.dll.decode().lower()
            for imp in e.imports:
                nom = (imp.name or b"?").decode()
                t = self._allouer_tramp(f"{dll}!{nom}")
                if imp.address:
                    uc.mem_write(BASE + imp.address - BASE,
                                 struct.pack("<Q", t))
        uc.mem_map(TRAMP, TRAMP_TAILLE)
        uc.mem_map(MAGIC_TRET, 0x1000)
        uc.mem_map(PILE, PILE_TAILLE * 8)
        uc.mem_map(SCRATCH, 0x10000)
        uc.mem_write(CMDLINE, LIGNE_CMD.encode("utf-16-le") + b"\x00\x00")

        # la séquence e3 : la sonde TCP (connexion morte) PUIS la sonde
        # d'armement (la requête en forme absolue qui sera ROUTÉE)
        sonde_tcp = self._nouvelle_socket("sonde-tcp")
        sonde_armement = self._nouvelle_socket("sonde-armement")
        self.sockets[sonde_tcp]["recus"] = [b""]
        self.sockets[sonde_armement]["recus"] = [REQUETE_SONDE, b""]
        self.accepts = [sonde_tcp, sonde_armement]
        self.ecoute = {"socket": None}

        uc.hook_add(UC_HOOK_CODE, self._crochet_code)
        uc.hook_add(UC_HOOK_MEM_INVALID, self._crochet_faute)

    def _allouer_tramp(self, cle: str) -> int:
        if cle in self.imp_par_nom:
            return self.imp_par_nom[cle]
        t = TRAMP + self.tramp_suivant["i"] * 0x20
        self.tramp_suivant["i"] += 1
        self.imp_par_nom[cle] = t
        return t

    def _nouvelle_socket(self, role: str) -> int:
        self.soc_suivant["n"] += 1
        s = self.soc_suivant["n"]
        self.sockets[s] = {"role": role, "recus": [], "ouvert": True}
        return s

    # ----------------------------------------------------------- registres
    def r(self, nom_reg: str) -> int:
        return self.uc.reg_read(globals()[f"UC_X86_REG_{nom_reg}"])

    def w(self, nom_reg: str, val: int) -> None:
        self.uc.reg_write(globals()[f"UC_X86_REG_{nom_reg}"], val)

    def sauver_contexte(self) -> dict:
        return {k: self.r(k) for k in REGS} | {"RIP": self.r("RIP")}

    def restaurer_contexte(self, ctx: dict) -> None:
        for k in REGS:
            self.w(k, ctx[k])
        self.w("RIP", ctx["RIP"])

    # ------------------------------------------------------------- chaînes
    def c_chaine(self, addr: int, maxo: int = 256) -> str:
        if not addr:
            return "(null)"
        brut = bytes(self.uc.mem_read(addr, maxo))
        k = brut.find(b"\x00")
        if k >= 0:
            brut = brut[:k]
        return brut.decode("latin-1", "replace")

    # ---------------------------------------------------------------- l'API
    def api_ret(self, valeur: int) -> None:
        self.w("RAX", valeur & 0xFFFFFFFFFFFFFFFF)
        self.w("RIP", struct.unpack("<Q", self.uc.mem_read(self.r("RSP"), 8))[0])
        self.w("RSP", self.r("RSP") + 8)

    def ecrire_ptr(self, addr: int, valeur: int, taille: int = 8) -> None:
        if addr:
            self.uc.mem_write(addr, valeur.to_bytes(taille, "little"))

    def api(self, nom: str) -> None:
        a1, a2, a3, a4 = self.r("RCX"), self.r("RDX"), self.r("R8"), self.r("R9")

        if nom == "kernel32!GetCommandLineW":
            self.appels.append("GetCommandLineW")
            self.api_ret(CMDLINE)

        elif nom == "kernel32!GetStdHandle":
            self.appels.append(f"GetStdHandle({a1})")
            self.api_ret(0xF00D0000 + (a1 & 0xF))

        elif nom == "kernel32!WriteFile":
            n = a3
            brut = bytes(self.uc.mem_read(a2, n)) if n else b""
            self.journal.append(brut)
            self.ecrire_ptr(a4, n)
            self.api_ret(1)

        elif nom == "kernel32!ReadFile":
            self.ecrire_ptr(a4, 0)
            self.api_ret(0)

        elif nom == "kernel32!ExitProcess":
            self.arret["code"] = a1
            self.arret["raison"] = "ExitProcess"
            self.appels.append(f"ExitProcess({a1})")
            self.uc.emu_stop()

        elif nom == "kernel32!CreateThread":
            start, param = a3, a4
            self.appels.append(f"CreateThread(start=0x{start:X}, param=0x{param:X})")
            ctx_parent = self.sauver_contexte()
            ret_addr = struct.unpack("<Q",
                                     self.uc.mem_read(ctx_parent["RSP"], 8))[0]
            ctx_parent["RSP"] += 8
            ctx_parent["RIP"] = ret_addr
            ctx_parent["RAX"] = 0x7E000000 + len(self.fils)
            self.fils.append({"start": start, "param": param, "ctx": ctx_parent})
            pile_haut = PILE + (len(self.fils) + 1) * PILE_TAILLE
            self.w("RSP", pile_haut - 8)
            self.uc.mem_write(pile_haut - 8, struct.pack("<Q", MAGIC_TRET))
            self.w("RCX", param)
            self.w("RAX", 0)
            self.w("RIP", start)

        elif nom == "kernel32!CloseHandle":
            self.api_ret(1)

        elif nom == "kernel32!VirtualProtect":
            self.ecrire_ptr(a4, 0x40, 4)
            self.api_ret(1)

        elif nom in ("kernel32!InitializeCriticalSection",
                     "kernel32!EnterCriticalSection",
                     "kernel32!LeaveCriticalSection"):
            self.api_ret(0)

        elif nom == "ws2_32!WSAStartup":
            self.uc.mem_write(a2, b"\x00" * 408)
            self.uc.mem_write(a2, struct.pack("<HH", 0x0202, 0x0202))
            self.appels.append("WSAStartup")
            self.api_ret(0)

        elif nom == "ws2_32!socket":
            s = self._nouvelle_socket(f"socket({a1},{a2},{a3})")
            if self.ecoute["socket"] is None and a2 == 1:
                self.ecoute["socket"] = s
            self.appels.append(f"socket({a1},{a2},{a3}) -> 0x{s:X}")
            self.api_ret(s)

        elif nom == "ws2_32!bind":
            self.appels.append(f"bind(0x{a1:X}, 0x{a2:X}, {a3})")
            self.api_ret(0)

        elif nom == "ws2_32!listen":
            self.appels.append(f"listen(0x{a1:X}, {a2})")
            self.api_ret(0)

        elif nom == "ws2_32!accept":
            if self.accepts:
                s = self.accepts.pop(0)
                self.appels.append(
                    f"accept(0x{a1:X}) -> 0x{s:X} ({self.sockets[s]['role']})")
                self.api_ret(s)
            else:
                # script épuisé : la boucle accept termine proprement
                self.appels.append("accept(0x{a1:X}) -> INVALID (script épuisé)")
                self.api_ret(0xFFFFFFFFFFFFFFFF)

        elif nom == "ws2_32!recv":
            s = a1
            st = self.sockets.get(s)
            if st and st["recus"]:
                morceau = st["recus"].pop(0)
            else:
                morceau = b""
            if morceau:
                self.uc.mem_write(a2, morceau)
                self.appels.append(f"recv(0x{s:X}) -> {len(morceau)} o")
                self.api_ret(len(morceau))
            else:
                self.appels.append(f"recv(0x{s:X}) -> 0 (pair fermé)")
                self.api_ret(0)

        elif nom == "ws2_32!send":
            s, n = a1, a3
            brut = bytes(self.uc.mem_read(a2, n)) if n else b""
            self.envois.setdefault(s, []).append(brut)
            self.appels.append(f"send(0x{s:X}, {n} o) : {brut[:60]!r}")
            self.api_ret(n)

        elif nom == "ws2_32!closesocket":
            self.appels.append(f"closesocket(0x{a1:X})")
            if a1 in self.sockets:
                self.sockets[a1]["ouvert"] = False
            self.api_ret(0)

        elif nom == "ws2_32!WSAGetLastError":
            self.api_ret(0)

        elif nom == "ws2_32!WSACleanup":
            self.appels.append("WSACleanup")
            self.api_ret(0)

        elif nom == "ws2_32!getaddrinfo":
            noeud = self.c_chaine(a1) if a1 else "(null)"
            service = self.c_chaine(a2) if a2 else "(null)"
            self.appels.append(f"getaddrinfo(noeud={noeud!r}, service={service!r})")
            z = GAI_ZONE
            sockaddr = (struct.pack("<HH", 2, 0xBB01)
                        + struct.pack(">I", 0x7F000001) + b"\x00" * 8)
            ai = struct.pack("<IIIIQQQQ", 0, 2, 1, 6, 16, 0, z + 64, 0)
            self.uc.mem_write(z, ai)
            self.uc.mem_write(z + 64, sockaddr)
            self.ecrire_ptr(a4, z)
            self.api_ret(0)

        elif nom == "ws2_32!freeaddrinfo":
            self.appels.append("freeaddrinfo")
            self.api_ret(0)

        elif nom == "ws2_32!connect":
            fam, port = struct.unpack("<HH", self.uc.mem_read(a2, 4))
            addr = struct.unpack(">I", self.uc.mem_read(a2 + 4, 4))[0]
            self.appels.append(f"connect(0x{a1:X}) -> {addr}:{(port >> 8) & 0xFF}"
                               f"{port & 0xFF} (fam={fam})")
            self.api_ret(0)

        elif nom.startswith("secur32!"):
            codes = {"AcquireCredentialsHandleW": 0, "FreeCredentialsHandle": 0,
                     "DeleteSecurityContext": 0}
            v = codes.get(nom.split("!")[1], 0x80090311)
            self.appels.append(f"{nom.split('!')[1]} -> 0x{v:X}")
            self.api_ret(v)

        else:
            self.appels.append(f"{nom} (non shimmé) -> 0")
            self.api_ret(0)

    # ---------------------------------------------------------- les crochets
    def _crochet_code(self, uc_, adresse, taille, _):
        if adresse == MAGIC_TRET:
            return
        if TRAMP <= adresse < TRAMP + TRAMP_TAILLE:
            cle = [k for k, v in self.imp_par_nom.items() if v == adresse]
            if cle:
                self.api(cle[0].replace(".dll!", "!"))
                return
        self.compteur["n"] += 1
        if self.compteur["n"] > BUDGET_INSTRUCTIONS:
            self.arret["raison"] = "budget d'instructions épuisé"
            uc_.emu_stop()
            return
        self.anneau.append(adresse)
        if len(self.anneau) > 48:
            self.anneau.pop(0)

    def _crochet_faute(self, uc_, acces, adresse, taille, valeur, _):
        rip = self.r("RIP")
        rva = rip - BASE
        self.arret["raison"] = (f"FAUTE MÉMOIRE acces={acces} adresse=0x{adresse:X} "
                                f"taille={taille}")
        self.pieces_faute = {
            "acces": acces, "adresse": adresse, "rip": rip, "rva": rva,
            "bloc": bloc_de(rva), "anneau": list(self.anneau),
        }
        try:
            brut = bytes(self.uc.mem_read(rip, 16))
            for i in self.md.disasm(brut, rip):
                self.pieces_faute["instruction"] = f"{i.mnemonic} {i.op_str}"
                break
        except Exception:
            self.pieces_faute["instruction"] = "(désassemblage impossible)"
        return False

    # ------------------------------------------------------------------- GO
    def executer(self) -> None:
        uc = self.uc
        pile_haut = PILE + PILE_TAILLE          # le fil principal
        uc.mem_write(pile_haut - 8, struct.pack("<Q", MAGIC_TRET))
        self.w("RSP", pile_haut - 8)            # entrée : rsp ≡ 8 (mod 16)
        self.w("RCX", 0)
        self.w("RDX", 0)
        self.w("RIP", BASE + self.pe.OPTIONAL_HEADER.AddressOfEntryPoint)

        import traceback
        while True:
            try:
                uc.emu_start(self.r("RIP"), MAGIC_TRET)
            except Exception as exc:  # noqa: BLE001
                if not self.arret["raison"]:
                    self.arret["raison"] = (f"exception émulation : "
                                            f"{type(exc).__name__} : {exc}")
                    traceback.print_exc()
                break
            if self.arret["raison"]:
                break
            if self.r("RIP") == MAGIC_TRET and self.fils:
                termine = self.fils.pop()
                self.restaurer_contexte(termine["ctx"])
                continue
            if self.r("RIP") == MAGIC_TRET:
                self.arret["raison"] = "fin naturelle (le fil principal a rendu la main)"
                break
            self.arret["raison"] = f"arrêt inexpliqué à RIP=0x{self.r('RIP'):X}"
            break


# ---------------------------------------------------------------- le verdict
def executer(chemin_exe: str | None = None, bavard: bool = True) -> tuple[bool, list[str]]:
    """-> (vert, lignes du bilan). VERT = D146 : requête routée SERVIE à la
    base réelle, crash nommé le cas échéant (fail-closed sur toute pièce
    manquante)."""
    chemin = pathlib.Path(chemin_exe) if chemin_exe else ICI / "proxy.exe"
    lignes: list[str] = []
    if not chemin.exists():
        return False, [f"[D146] ERREUR FATALE : artefact introuvable : {chemin}"]
    try:
        ctl = ControleBaseReelle(chemin)
    except Exception as exc:  # noqa: BLE001
        return False, [f"[D146] ERREUR FATALE : image illisible : {exc}"]
    ctl.executer()

    journal_txt = b"".join(ctl.journal).decode("latin-1", "replace")
    faute = getattr(ctl, "pieces_faute", None)

    # (a) AUCUNE faute mémoire — sinon NOMMÉE (adresse, instruction, bloc)
    vert = True
    lignes.append(f"[D146] contrôle d'exécution full-PE — base réelle {BASE:#x}, "
                  f"artefact {chemin.name} ({len(ctl.data)} o)")
    lignes.append(f"[D146] arrêt : {ctl.arret['raison'] or 'fin naturelle'}"
                  + (f", code {ctl.arret['code']}" if ctl.arret['code'] is not None else "")
                  + f" — {ctl.compteur['n']} instructions")
    if faute:
        vert = False
        lignes.append(f"[D146] KO (a) — FAUTE MÉMOIRE NOMMÉE : acces={faute['acces']} "
                      f"adresse=0x{faute['adresse']:X}")
        lignes.append(f"[D146]   RIP=0x{faute['rip']:X} (RVA 0x{faute['rva']:X} — "
                      f"{faute['bloc']}) sur : {faute.get('instruction', '?')}")
        dern = faute["anneau"][-6:]
        lignes.append("[D146]   anneau (6 dernières) : "
                      + " ".join(f"0x{a - BASE:X}" for a in dern))

    # (b) la ligne de flux ÉMISE, méthode en TEXTE (le point du correctif)
    ligne_flux = [l.strip() for l in journal_txt.splitlines()
                  if l.strip().startswith("flux ")]
    if ligne_flux:
        if " flux GET " in " " + ligne_flux[0] + " " or "GET" in ligne_flux[0]:
            lignes.append(f"[D146] (b) ligne de flux ÉMISE : « {ligne_flux[0]} » "
                          f"— méthode lue de R_TAB_METHODES à la base réelle")
        else:
            vert = False
            lignes.append(f"[D146] KO (b) — ligne de flux sans méthode texte : "
                          f"« {ligne_flux[0]} »")
    else:
        vert = False
        lignes.append("[D146] KO (b) — AUCUNE ligne de flux dans le journal "
                      "(la requête routée n'a pas traversé la session)")

    # (c) le client a reçu une réponse sur la socket routée
    recus = {s: b"".join(m) for s, m in ctl.envois.items()}
    if recus:
        for s, m in recus.items():
            role = ctl.sockets.get(s, {}).get("role", "?")
            lignes.append(f"[D146] (c) client servi [socket 0x{s:X} {role}] : "
                          f"{len(m)} o : {m[:80]!r}")
    else:
        vert = False
        lignes.append("[D146] KO (c) — AUCUN octet envoyé au client "
                      "(requête routée non servie)")

    if vert:
        lignes.append("[D146] VERDICT VERT — la requête routée est SERVIE à la "
                      "base réelle de l'image ; le scellage peut être jugé "
                      "sur ce témoin (D146)")
    else:
        lignes.append("[D146] VERDICT KO — pièces nommées ci-dessus ; "
                      "AUCUN scellage rc/final dans cet état (D146)")

    if bavard:
        print("=" * 72)
        for l in lignes:
            print(l)
        print("-" * 72)
        print("JOURNAL STDOUT CAPTÉ :")
        for l in journal_txt.splitlines():
            print(f"  | {l}")
        print("-" * 72)
        print(f"TRACE API ({len(ctl.appels)} appels, 40 derniers) :")
        for a in ctl.appels[-40:]:
            print(f"  {a}")
    return vert, lignes


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Contrôle D146 : exécution full-PE "
                                            "à la base réelle")
    p.add_argument("--chemin", default=str(ICI / "proxy.exe"),
                   help="chemin de l'artefact à contrôler (défaut : m5/proxy.exe)")
    args = p.parse_args()
    ok, _ = executer(args.chemin, bavard=True)
    sys.exit(0 if ok else 1)
