#!/usr/bin/env python3
"""oracle_demo.py — Oracle différentiel du jalon démo (D1 : éphémère, régénéré).

Dérivé de la couche I de la démo (demo/I/*.md). Cinq familles :

  1. MODÈLE CHARGEUR (D35) : l'IAT est résolue aux FirstThunk des descripteurs
     — exactement comme Windows, kernel32#2 compris (D36) — et le verrou exige
     que CHAQUE slot appelé par la notation soit couvert.
  2. BLOCS : win-05 (paire EM_SETSEL/EM_REPLACESEL + MIROIR FICHIER, texte
     exact), win-06 (image saine -> 4 ; version sous plancher -> -1), win-07
     (connect ok/échec + closesocket), win-08 (écoute publiée, spawn tcp-09,
     arrêt), win-11 (journal fichier : modes ASCII/valeur/UTF-16, chemin à
     côté de l'exe, paresse, re-tentative après échec).
  3. COQUILLE GUI RÉELLE (D36 — le durcissement) : win-01 est exécuté depuis
     le point d'entrée : RegisterClassExW VALIDÉ (cbSize, wndproc dans
     l'image, nom de classe), CreateWindowExW TOP-NIVEAU dispatche VRAIMENT
     WM_CREATE puis WM_SIZE à la procédure (appels imbriqués pilotés par le
     moteur), les contrôles enfants sont créés, la GÉOMÉTRIE MoveWindow est
     VÉRIFIÉE (largeur/hauteur > 0 — le défaut D36 de demo.1, fenêtre vide,
     est impossible à réintroduire), le journal fichier contient L00/L02/L01
     dans l'ordre, ExitProcess(0) constaté. Puis clic (WM_COMMAND) : thread
     scénario lancé UNE fois, second clic ignoré. Échec piloté : classe en
     échec -> MessageBoxW + LKO…gle=NN + sortie 1.
  4. SCÉNARIO COMPLET (win-09) : le patch tcp-07 s'exécute RÉELLEMENT en
     émulation ; le journal ÉCRAN (11 lignes nominales) ET le journal FICHIER
     (miroir Latin-1) sont comparés exactement ; rollback et arrêt propre
     constatés.
  5. FALSIFICATION : (a) octets de chaque bloc embarqué corrompus -> la porte
     R10 (win-06) les détecte tous — zéro silence ; (b) FALSIFICATION RECT :
     l'octet de déplacement de la lecture RECT.right (0x28) réécrit en 0x24
     — le défaut D36 originel — la coquille GUI doit ÉCHOUER (V4 de win-04).
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import importlib.util as _ilu
if "layout_demo" in sys.modules:
    L = sys.modules["layout_demo"]
else:
    _spec = _ilu.spec_from_file_location("layout_demo", os.path.join(ICI, "layout.py"))
    L = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(L)
    sys.modules["layout_demo"] = L

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_RSP, UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX,
    UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP, UC_X86_REG_EFLAGS,
    UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP,
    UC_X86_REG_R10, UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13,
    UC_X86_REG_R14, UC_X86_REG_R15)

IMAGE = L.IMAGE_BASE
PILE_BASE, PILE_TAILLE = 0x700000000, 0x100000
TRAMPOLINE = 0x600000000
SENTINELLE = 0x500000000
FAKE_SOCK, FAKE_STDOUT = 0x1111, 0x99
FAKE_HANDLE_FICHIER = 0xABCD

TOUTES_API = (list(L.KERNEL32_IMPORTS) + list(L.KERNEL32B_IMPORTS)
              + list(L.WS2_IMPORTS)
              + list(L.USER32_IMPORTS) + list(L.GDI32_IMPORTS))
FAUX = {nom: TRAMPOLINE + i * 0x10 for i, nom in enumerate(TOUTES_API)}
FAUX_REV = {v: k for k, v in FAUX.items()}

# Adresses des blocs démo dérivées du plan (aucun RVA codé en dur)
RVA_WIN = {spec.split(":")[0]: rva for _, spec, rva, _, _, _ in L.BLOCS_WIN}

REGS_CONTEXTE = (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                 UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP, UC_X86_REG_RSP,
                 UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                 UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
                 UC_X86_REG_RIP, UC_X86_REG_EFLAGS)


class EchecOracle(Exception):
    pass


def latin1(texte: str) -> bytes:
    """Conversion win-11 mode 2 (référence) : → devient '>', ≥ 0x100 '-'."""
    sortie = bytearray()
    for ch in texte:
        cp = ord(ch)
        if cp == 0x2192:
            sortie.append(0x3E)
        elif cp >= 0x100:
            sortie.append(0x2D)
        else:
            sortie.append(cp & 0xFF)
    return bytes(sortie)


class Emulateur:
    """Une instance = demo.exe mappé ; shims IAT scriptés (pattern oracle M2).

    Moteur D36 : les shims peuvent METTRE EN ATTENTE des appels de procédure
    de fenêtre (CreateWindowExW top-niveau → WM_CREATE/WM_SIZE) — le moteur
    d'exécution sauve le contexte, exécute la procédure en pile séparée,
    restaure le contexte puis simule le retour de l'API.
    """

    def __init__(self, exe: bytes):
        self.exe = bytes(exe)
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(IMAGE, L.SIZE_OF_IMAGE)
        uc.mem_map(PILE_BASE, PILE_TAILLE)
        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_map(SENTINELLE, 0x1000)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)
        uc.mem_write(SENTINELLE, b"\xc3" * 0x1000)
        self._crochet_pose = False
        self.reinit()

    def _ecrire_image(self):
        uc = self.uc
        uc.mem_write(IMAGE + L.TEXT_RVA, self.exe[L.TEXT_FILE:L.TEXT_FILE + L.TEXT_VSIZE])
        uc.mem_write(IMAGE + L.RDATA_RVA, self.exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE])
        uc.mem_write(IMAGE + L.DATA_RVA, self.exe[L.DATA_FILE:L.DATA_FILE + L.DATA_RAW])
        uc.mem_write(IMAGE + L.TEXT2_RVA, self.exe[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE])
        uc.ctl_remove_cache(IMAGE + L.TEXT_RVA, IMAGE + L.TEXT_RVA + L.TEXT_VSIZE)
        uc.ctl_remove_cache(IMAGE + L.TEXT2_RVA, IMAGE + L.TEXT2_RVA + L.TEXT2_VSIZE)

    def reinit(self):
        """Image + .data vierge + IAT résolue PAR LE MODÈLE CHARGEUR (D35/D36)."""
        self._ecrire_image()
        self.uc.mem_write(IMAGE + L.DATA_RVA, b"\x00" * L.DATA_VSIZE)
        rdata = self.exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]

        def cstr(rva):
            fin = rdata.index(b"\x00", rva - L.RDATA_RVA)
            return rdata[rva - L.RDATA_RVA:fin].decode("ascii")

        for rva_desc in (L.R_DESC_IMPORT, L.R_DESC_WS2, L.R_DESC_USER32,
                         L.R_DESC_GDI32, L.R_DESC_K32B):
            oft, _, _, nom_dll, ft = struct.unpack_from(
                "<IIIII", rdata, rva_desc - L.RDATA_RVA)
            if not (oft or ft):
                continue
            i = 0
            while True:
                hint_rva = struct.unpack_from("<Q", rdata, oft - L.RDATA_RVA + 8 * i)[0]
                if hint_rva == 0:
                    break
                nom = cstr(hint_rva + 2)
                if nom not in FAUX:
                    raise EchecOracle(f"chargeur : import inconnu : {nom_dll}!{nom}")
                self.uc.mem_write(IMAGE + ft + 8 * i, struct.pack("<Q", FAUX[nom]))
                i += 1
        for nom, rva in L.IAT_SLOTS.items():          # verrou D35
            val = struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]
            if val != FAUX[nom]:
                raise EchecOracle(f"chargeur/D35 : slot {nom} @{rva:#x} non résolu "
                                  f"({val:#x}) — FirstThunk divergent (T3)")
        # état d'émulation
        self.journal: list[str] = []            # journal ÉCRAN (EM_REPLACESEL)
        self.journal_fichier: list[bytes] = []  # journal FICHIER (WriteFile, lignes)
        self.envois: list[bytes] = []
        self.threads: list[tuple] = []
        self.handles_fermes: list[int] = []
        self.fermetures: list[int] = []
        self.file_accept = [0x777, -1]
        self.retour_connect = 0
        self.retour_socket = FAKE_SOCK
        # GUI (D36)
        self.classes: dict[str, tuple] = {}     # nom -> (wndproc, hInstance)
        self.movewindow: list[tuple] = []
        self.sendmessages: list[tuple] = []
        self.messageboxes: list[tuple] = []
        self.enablewindows: list[tuple] = []
        self.hwnd_suivant = 0x3000
        self.retour_register = 0x1234           # atome (0 = échec piloté)
        self.retour_createwindow = None         # None = réel ; 0 = échec piloté
        # fichiers (D36)
        self.chemin_ouvert: str | None = None
        self.createfile_appels: list[str] = []
        self.retour_createfile = FAKE_HANDLE_FICHIER   # -1 = échec piloté
        self.gle = 0                            # valeur du shim GetLastError
        # moteur
        self.pending: list[tuple] = []
        self.pending_retour: tuple | None = None
        self.sortie = False
        self.code_sortie: int | None = None

    def qword(self, rva):
        return struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]

    # --- shims -----------------------------------------------------------------

    def installer_shims(self):
        if self._crochet_pose:
            return
        self._crochet_pose = True

        def retour(uc_):
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            adr = struct.unpack("<Q", uc_.mem_read(rsp, 8))[0]
            uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc_.reg_write(UC_X86_REG_RIP, adr)

        def arg_pile(uc_, n, taille=8):
            """n-ième argument (5+) : [rsp + 0x28 + 8*(n-5)] au moment du crochet."""
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            brut = uc_.mem_read(rsp + 0x28 + 8 * (n - 5), taille)
            return struct.unpack("<Q" if taille == 8 else "<I", brut)[0]

        def chaine_utf16(uc_, adr, maxchars=64):
            brut = bytes(uc_.mem_read(adr, 2 * maxchars))
            fin = brut.find(b"\x00\x00")
            if fin % 2:
                fin += 1
            return brut[:fin if fin >= 0 else 2 * maxchars].decode("utf-16-le")

        def chaine_ascii(uc_, adr, maxo=280):
            brut = bytes(uc_.mem_read(adr, maxo))
            return brut[:brut.find(b"\x00")].decode("ascii", errors="replace")

        def i32(v):
            return v - 0x100000000 if v & 0x80000000 else v

        def crochet(uc_, adresse, taille, _):
            nom = FAUX_REV.get(adresse)
            if nom is None:
                return
            rcx = uc_.reg_read(UC_X86_REG_RCX)
            rdx = uc_.reg_read(UC_X86_REG_RDX)
            r8 = uc_.reg_read(UC_X86_REG_R8)
            r9 = uc_.reg_read(UC_X86_REG_R9)
            if nom == "GetStdHandle":
                c = rcx & 0xFFFFFFFF
                uc_.reg_write(UC_X86_REG_RAX, FAKE_STDOUT if c == 0xFFFFFFF5 else 0x98)
            elif nom == "CloseHandle":
                self.handles_fermes.append(rcx)
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "CreateThread":
                self.threads.append((r8, r9))
                uc_.reg_write(UC_X86_REG_RAX, 0x100 + 8 * len(self.threads))
            elif nom == "VirtualProtect":
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "GetLastError":
                uc_.reg_write(UC_X86_REG_RAX, self.gle & 0xFFFFFFFF)
            elif nom == "GetModuleFileNameA":
                chemin = b"C:\\demo\\demo.exe\x00"
                uc_.mem_write(rdx, chemin)
                uc_.reg_write(UC_X86_REG_RAX, len(chemin) - 1)
            elif nom == "CreateFileA":
                chemin = chaine_ascii(uc_, rcx)
                self.createfile_appels.append(chemin)
                self.chemin_ouvert = chemin
                uc_.reg_write(UC_X86_REG_RAX,
                              self.retour_createfile & 0xFFFFFFFFFFFFFFFF)
            elif nom == "WriteFile":
                if rcx == FAKE_HANDLE_FICHIER:
                    n = r8 & 0xFFFFFFFF
                    self.journal_fichier.append(bytes(uc_.mem_read(rdx, n)))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "FlushFileBuffers":
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom in ("InitializeCriticalSection", "EnterCriticalSection",
                         "LeaveCriticalSection", "WSAStartup", "bind", "listen",
                         "WSACleanup", "WSAGetLastError", "TranslateMessage",
                         "DispatchMessageW", "PostQuitMessage", "DestroyWindow",
                         "DefWindowProcW"):
                uc_.reg_write(UC_X86_REG_RAX, 1 if nom in
                              ("DestroyWindow", "DefWindowProcW") else 0)
            elif nom == "EnableWindow":
                self.enablewindows.append((rcx, rdx & 0xFFFFFFFF))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "GetModuleHandleW":
                uc_.reg_write(UC_X86_REG_RAX, IMAGE)
            elif nom == "LoadCursorW":
                uc_.reg_write(UC_X86_REG_RAX, 0x7788)
            elif nom == "GetStockObject":
                uc_.reg_write(UC_X86_REG_RAX, 0x5566)
            elif nom == "GetClientRect":
                # lpRect = rdx (rcx = hwnd) — défaut latent de l'oracle R1 :
                # jamais exécuté avant la coquille GUI réelle (D36).
                uc_.mem_write(rdx, struct.pack("<iiii", 0, 0, 780, 560))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "RegisterClassExW":
                cbsize, style = struct.unpack_from("<II", uc_.mem_read(rcx, 16))
                wndproc, = struct.unpack_from("<Q", uc_.mem_read(rcx + 8, 8))
                nom_classe = chaine_utf16(uc_, struct.unpack_from(
                    "<Q", uc_.mem_read(rcx + 64, 8))[0])
                if cbsize != 0x50 or not (IMAGE <= wndproc < IMAGE + L.SIZE_OF_IMAGE) \
                        or self.retour_register == 0:
                    uc_.reg_write(UC_X86_REG_RAX, 0)
                else:
                    self.classes[nom_classe] = (wndproc, 0)
                    uc_.reg_write(UC_X86_REG_RAX, self.retour_register)
            elif nom == "MessageBoxW":
                self.messageboxes.append((chaine_utf16(uc_, rdx),
                                          chaine_utf16(uc_, r8)))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "SendMessageW":
                msg = rdx & 0xFFFFFFFF
                self.sendmessages.append((rcx, msg, r8, r9))
                if msg == 0xC2:                            # EM_REPLACESEL
                    brut = bytes(uc_.mem_read(r9, 512))
                    fin = 0
                    while fin + 1 < len(brut) and brut[fin:fin + 2] != b"\x00\x00":
                        fin += 2
                    texte = brut[:fin].decode("utf-16-le", errors="replace")
                    self.journal.append(texte)
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "MoveWindow":
                # D36 : INVARIANT GÉOMÉTRIQUE — le défaut « largeur = -16 »
                # (demo.1) est rejeté ici, pas seulement constaté.
                x, y, l, h = i32(rdx & 0xFFFFFFFF), i32(r8 & 0xFFFFFFFF), \
                    i32(r9 & 0xFFFFFFFF), i32(arg_pile(uc_, 5, 4))
                if x < 0 or y < 0 or l <= 0 or h <= 0:
                    raise EchecOracle(
                        f"MoveWindow : géométrie invalide (x={x}, y={y}, "
                        f"largeur={l}, hauteur={h}) — défaut de classe D36")
                self.movewindow.append((rcx, x, y, l, h))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "CreateWindowExW":
                if self.retour_createwindow == 0:
                    uc_.reg_write(UC_X86_REG_RAX, 0)
                else:
                    classe = chaine_utf16(uc_, rdx)
                    parent = arg_pile(uc_, 9)
                    style = r9 & 0xFFFFFFFF
                    if parent or (style & 0x40000000):    # contrôle enfant
                        if classe not in ("EDIT", "BUTTON"):
                            uc_.reg_write(UC_X86_REG_RAX, 0)
                            retour(uc_)
                            return
                        self.hwnd_suivant += 1
                        uc_.reg_write(UC_X86_REG_RAX, self.hwnd_suivant)
                    elif classe in self.classes:          # fenêtre top-niveau
                        wndproc, _ = self.classes[classe]
                        self.hwnd_suivant += 1
                        hwnd = self.hwnd_suivant
                        param = arg_pile(uc_, 12)
                        # dispatch réel : WM_CREATE puis WM_SIZE (D36)
                        self.pending.append((wndproc, (hwnd, 1, 0, param)))
                        self.pending.append((wndproc, (hwnd, 5, 0, 0)))
                        self.pending_retour = ("fenetre", hwnd)
                        uc_.emu_stop()
                        return
                    else:
                        uc_.reg_write(UC_X86_REG_RAX, 0)   # classe non enregistrée
            elif nom == "GetMessageW":
                uc_.reg_write(UC_X86_REG_RAX, 0)          # WM_QUIT immédiat
            elif nom == "ExitProcess":
                self.code_sortie = rcx & 0xFFFFFFFF
                self.sortie = True
                uc_.emu_stop()
                return
            elif nom == "socket":
                uc_.reg_write(UC_X86_REG_RAX, self.retour_socket)
            elif nom == "connect":
                self.appels_connect = getattr(self, "appels_connect", []) + [rcx]
                uc_.reg_write(UC_X86_REG_RAX, self.retour_connect & 0xFFFFFFFF)
            elif nom == "closesocket":
                self.fermetures.append(rcx)
                uc_.reg_write(UC_X86_REG_RAX, 0)
            elif nom == "accept":
                if not self.file_accept:
                    uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                else:
                    item = self.file_accept.pop(0)
                    uc_.reg_write(UC_X86_REG_RAX,
                                  item if item >= 0 else 0xFFFFFFFFFFFFFFFF)
            elif nom == "send":
                n = r8 & 0xFFFFFFFF
                self.envois.append(bytes(uc_.mem_read(rdx, n)))
                uc_.reg_write(UC_X86_REG_RAX, n)
            elif nom == "recv":
                # Le serveur (thread simulé absent) reflète l'état RÉEL du patch :
                # la cohérence bascule -> réponse est ainsi vérifiée de bout en
                # bout — si le trampoline n'avait pas basculé, le scénario
                # recevrait la minuscule et échouerait au memcmp.
                n = r8 & 0xFFFFFFFF
                etat = struct.unpack("<Q", uc_.mem_read(IMAGE + L.R_ETAT_PATCH, 8))[0]
                reponse = L.PHRASE_MAJ if etat == 1 else L.PHRASE
                uc_.mem_write(rdx, reponse[:n])
                uc_.reg_write(UC_X86_REG_RAX, len(reponse[:n]))
            else:
                raise EchecOracle(f"shim non implémenté : {nom}")
            retour(uc_)

        self.uc.hook_add(UC_HOOK_CODE, crochet, begin=TRAMPOLINE, end=TRAMPOLINE + 0x1000)

    # --- moteur d'exécution (pilotage des appels imbriqués, D36) ----------------

    def _sauver_contexte(self):
        return {r: self.uc.reg_read(r) for r in REGS_CONTEXTE}

    def _restaurer_contexte(self, ctx):
        for r, v in ctx.items():
            self.uc.reg_write(r, v)

    def appeler(self, rva: int, args: tuple = (), limite: int = 5_000_000,
                pile: int = 0x80000):
        uc = self.uc
        if pile == 0x80000:
            self.sortie = False          # un appel de haut niveau repart proprement
        rsp = PILE_BASE + pile
        for i, a in enumerate(args):
            if i < 4:
                uc.reg_write((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                              UC_X86_REG_R9)[i], a)
            else:
                uc.mem_write(rsp + 0x20 + 8 * (i - 4), struct.pack("<Q", a))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp, struct.pack("<Q", SENTINELLE))
        uc.reg_write(UC_X86_REG_RIP, IMAGE + rva)
        debut = IMAGE + rva
        budget = limite
        while budget > 0:
            pas = min(budget, 500_000)
            uc.emu_start(debut, SENTINELLE, timeout=0, count=pas)
            budget -= pas
            rip = uc.reg_read(UC_X86_REG_RIP)
            if self.sortie or rip == SENTINELLE:
                break
            if self.pending:
                # dispatch GUI réel : sauver, exécuter la procédure (pile
                # séparée), restaurer, simuler le retour de l'API.
                ctx = self._sauver_contexte()
                resultats = []
                while self.pending:
                    fn, a = self.pending.pop(0)
                    resultats.append(self.appeler(fn - IMAGE, a, limite=limite,
                                                  pile=0xC0000))
                self._restaurer_contexte(ctx)
                rax = 0
                if self.pending_retour is not None:
                    type_attente, hwnd = self.pending_retour
                    if type_attente == "fenetre":
                        echec = any((r & 0xFFFFFFFF) == 0xFFFFFFFF
                                    for r in resultats[:1])
                        rax = 0 if echec else hwnd
                    self.pending_retour = None
                rsp_c = uc.reg_read(UC_X86_REG_RSP)
                retadr = struct.unpack("<Q", uc.mem_read(rsp_c, 8))[0]
                uc.reg_write(UC_X86_REG_RSP, rsp_c + 8)
                uc.reg_write(UC_X86_REG_RIP, retadr)
                uc.reg_write(UC_X86_REG_RAX, rax)
                debut = retadr
                continue
            debut = rip                                   # budget de pas épuisé
        return uc.reg_read(UC_X86_REG_RAX)


# --- Références dérivées de la couche I ----------------------------------------------

LIGNES_NOMINALES = ["J_ENTETE", "J_PROTO", "J_PORTE_OK", "J_LIBC_OK", "J_MEC_OK",
                    "J_SRV_OK", "J_CLI_OK", "J_ECHO_OK", "J_PROD_OK", "J_RB_OK", "J_FINAL"]

TRACE_L00 = L.CHAINES_ASCII["L00"][1] + b"\r\n"
TRACE_L01 = L.CHAINES_ASCII["L01"][1] + b"\r\n"
TRACE_L02 = L.CHAINES_ASCII["L02"][1] + b"\r\n"
TRACE_L03 = L.CHAINES_ASCII["L03"][1] + b"\r\n"
TRACE_L4C = L.CHAINES_ASCII["L4C"][1] + b"1\r\n"     # shim MoveWindow → 1 (D37)
TRACE_L4D = L.CHAINES_ASCII["L4D"][1] + b"1\r\n"
# Écran attendu au démarrage (miroir D37) : L02 puis L4C/L4D (WM_SIZE imbriqué
# dans CreateWindowExW) puis L01 — L00 sautée (HWND_JOURNAL encore nul, E1 win-05)
ECRAN_DEMARRAGE = [L.CHAINES_ASCII["L02"][1].decode("ascii") + "\r\n",
                   L.CHAINES_ASCII["L4C"][1].decode("ascii") + "1\r\n",
                   L.CHAINES_ASCII["L4D"][1].decode("ascii") + "1\r\n",
                   L.CHAINES_ASCII["L01"][1].decode("ascii") + "\r\n"]
FAKE_HWND_EDIT = 0x9988


def _fichier_rva(rva: int) -> int:
    if rva >= L.TEXT2_RVA:
        return L.TEXT2_FILE + (rva - L.TEXT2_RVA)
    if rva >= L.DATA_RVA:
        return L.DATA_FILE + (rva - L.DATA_RVA)
    if rva >= L.RDATA_RVA:
        return L.RDATA_FILE + (rva - L.RDATA_RVA)
    return L.TEXT_FILE + (rva - L.TEXT_RVA)


def _blocs():
    herit = [("a10002", 0x1040), ("a10003", 0x1080), ("b20001", 0x1100),
             ("b20002", 0x1180), ("b20003", 0x1200), ("b20004", 0x1280),
             ("c30001", 0x4000), ("c30002", 0x4100), ("c30003", 0x4140),
             ("c30004", 0x4180), ("c30005", 0x41C0), ("c30006", 0x4300),
             ("c30007", 0x4400), ("c30008", 0x4600), ("c30009", 0x4800),
             ("c30011", 0x4B00)]
    win = [(bid, rva) for bid, _, rva, slot, _, _ in L.BLOCS_WIN]
    return herit + win


def executer(exe: bytes, graine: int = 1) -> dict:
    total, verdicts = 0, {}

    # --- win-06 : porte R10 + vecteurs libc (image saine) ---
    em = Emulateur(exe)
    em.installer_shims()
    r = em.appeler(RVA_WIN["win-06"])
    if r != 4:
        raise EchecOracle(f"win-06 : eax = {r} != 4 (porte + 4 vecteurs attendus)")
    verdicts["d40006"] = {"cas": 5, "detail": "porte R10 verte + 4/4 vecteurs libc"}
    total += 5

    mutant = bytearray(exe)
    struct.pack_into("<Q", mutant, L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA), 0x00020000)
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    if em.appeler(RVA_WIN["win-06"]) != 0xFFFFFFFF:
        raise EchecOracle("win-06 : version sous plancher non détectée (E2)")
    total += 1

    # --- win-05 : miroir universel — entrée scénario (mode 2) ET entrée trace ---
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    adr, txt, n = L.CHAINES_UTF16["J_ENTETE"]
    em.appeler(L.JOURNAL_GUI, (IMAGE + adr, n))   # entrée scénario (shim mode 2)
    if em.journal != [txt]:
        raise EchecOracle(f"win-05 : journal {em.journal!r} != [{txt!r}]")
    if em.journal_fichier != [latin1(txt)]:
        raise EchecOracle(f"win-05 : miroir fichier {em.journal_fichier!r} != "
                          f"[{latin1(txt)!r}] (Q2 R3)")
    # entrée trace (JOURNAL_TRACE 0x5008) : mode 0 puis mode 1 (valeur)
    a01, o01, _ = L.CHAINES_ASCII["L01"]
    em.appeler(L.JOURNAL_TRACE, (IMAGE + a01, len(o01), 0, 0))
    if em.journal[-1] != o01.decode("ascii") + "\r\n":
        raise EchecOracle(f"win-05 trace mode 0 : écran {em.journal[-1]!r} != "
                          f"{o01.decode('ascii') + chr(13) + chr(10)!r} (Q1 R3)")
    ako, oko, _ = L.CHAINES_ASCII["LKO_GUI"]
    em.appeler(L.JOURNAL_TRACE, (IMAGE + ako, len(oko), 1, 87))
    attendu_ko = oko.decode("ascii") + "87\r\n"
    if em.journal[-1] != attendu_ko:
        raise EchecOracle(f"win-05 trace mode 1 : écran {em.journal[-1]!r} != "
                          f"{attendu_ko!r} (valeur itoa appendée, Q1 R3)")
    if em.journal_fichier[-2:] != [o01 + b"\r\n", oko + b"87\r\n"]:
        raise EchecOracle(f"win-05 trace : fichier {em.journal_fichier[-2:]!r} "
                          f"— relais win-11 (ptr, len, mode, valeur) altéré")
    # garde E1 : HWND_JOURNAL nul → miroir écran sauté, fichier intact
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", 0))
    avant = len(em.journal)
    em.appeler(L.JOURNAL_TRACE, (IMAGE + a01, len(o01), 0, 0))
    if len(em.journal) != avant or em.journal_fichier[-1] != o01 + b"\r\n":
        raise EchecOracle("win-05 : garde HWND nul ineffective (E1 R3)")
    verdicts["d40005"] = {"cas": 5, "detail": "entrée scénario + entrée trace "
                                               "(modes 0/1/valeur), écran+fichier, garde E1"}
    total += 5

    # --- win-11 : journal fichier (modes, chemin, paresse, re-tentative) ---
    em = Emulateur(exe)
    em.installer_shims()
    if em.createfile_appels:
        raise EchecOracle("win-11 : ouverture avant la première ligne (I1)")
    a01, o01, _ = L.CHAINES_ASCII["L01"]
    r = em.appeler(RVA_WIN["win-11"], (IMAGE + a01, len(o01), 0, 0))
    ako, oko, _ = L.CHAINES_ASCII["LKO_GUI"]
    r2 = em.appeler(RVA_WIN["win-11"], (IMAGE + ako, len(oko), 1, 1400))
    if em.chemin_ouvert != "C:\\demo\\demo_journal.txt":
        raise EchecOracle(f"win-11 : chemin {em.chemin_ouvert!r} != attendu "
                          f"(scan du répertoire de l'exe, Q3)")
    attendu = [o01 + b"\r\n", oko + b"1400\r\n"]
    if em.journal_fichier != attendu or (r, r2) != (1, 1):
        raise EchecOracle(f"win-11 : fichier {em.journal_fichier!r} != {attendu!r}")
    em.retour_createfile = -1                      # échec piloté (E2)
    em.uc.mem_write(IMAGE + L.R_JOURNAL_HANDLE, struct.pack("<Q", 0))
    if em.appeler(RVA_WIN["win-11"], (IMAGE + a01, len(o01), 0, 0)) != 0:
        raise EchecOracle("win-11 : échec CreateFileA non propagé (Q4)")
    if em.qword(L.R_JOURNAL_HANDLE) != 0xFFFFFFFFFFFFFFFF:
        raise EchecOracle("win-11 : handle non marqué en échec (Q4)")
    n_avant = len(em.journal_fichier)
    em.retour_createfile = FAKE_HANDLE_FICHIER     # re-tentative (Q4)
    if em.appeler(RVA_WIN["win-11"], (IMAGE + a01, len(o01), 0, 0)) != 1 \
            or len(em.journal_fichier) != n_avant + 1:
        raise EchecOracle("win-11 : re-tentative après échec absente (Q4)")
    a16, t16, n16 = L.CHAINES_UTF16["J_ENTETE"]
    em.appeler(RVA_WIN["win-11"], (IMAGE + a16, n16, 2, 0))
    if em.journal_fichier[-1] != latin1(t16):
        raise EchecOracle(f"win-11 : conversion UTF-16 {em.journal_fichier[-1]!r} "
                          f"!= {latin1(t16)!r} (mode 2)")
    verdicts["d40011"] = {"cas": 6, "detail": "modes 0/1/2, chemin exe, paresse, "
                                               "échec + re-tentative, Latin-1"}
    total += 6

    # --- win-07 : connect ok / échec ---
    em = Emulateur(exe)
    em.installer_shims()
    if em.appeler(RVA_WIN["win-07"]) != FAKE_SOCK:
        raise EchecOracle("win-07 : socket attendue (Q1)")
    em = Emulateur(exe)
    em.installer_shims()
    em.retour_connect = -1
    if em.appeler(RVA_WIN["win-07"]) != 0 or em.fermetures != [FAKE_SOCK]:
        raise EchecOracle("win-07 : échec connect non propagé (Q2/E2)")
    verdicts["d40007"] = {"cas": 2, "detail": "connect ok/échec, closesocket sur échec"}
    total += 2

    # --- win-08 : écoute publiée, spawn tcp-09, arrêt propre ---
    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(RVA_WIN["win-08"])
    if em.qword(L.R_LISTEN) != FAKE_SOCK or em.qword(L.DRAPEAU_SRV) != 1:
        raise EchecOracle("win-08 : écoute/drapeau non publiés (Q2)")
    if em.threads != [(IMAGE + 0x4800, 0x777)]:
        raise EchecOracle(f"win-08 : spawn tcp-09 attendu, obtenu {em.threads}")
    verdicts["d40008"] = {"cas": 3, "detail": "tcp-01 ok, R_LISTEN+drapeau, spawn tcp-09, arrêt"}
    total += 3

    # --- COQUILLE GUI RÉELLE (D36) : win-01 du point d'entrée à ExitProcess ---
    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(RVA_WIN["win-01"])
    if em.code_sortie != 0:
        raise EchecOracle(f"coquille GUI : sortie {em.code_sortie} != 0")
    if not (em.qword(L.HWND_PRINCIPAL) and em.qword(L.HWND_JOURNAL)
            and em.qword(L.HWND_BOUTON)):
        raise EchecOracle("coquille GUI : handles absents (fenêtre/contrôles)")
    hwnd_j, hwnd_b = em.qword(L.HWND_JOURNAL), em.qword(L.HWND_BOUTON)
    if em.movewindow != [(hwnd_j, 8, 8, 764, 504), (hwnd_b, 8, 516, 764, 36)]:
        raise EchecOracle(f"coquille GUI : géométrie {em.movewindow} — attendu "
                          f"journal (8,8,764,504), bouton (8,516,764,36) (V3 D36)")
    if em.journal_fichier != [TRACE_L00, TRACE_L02, TRACE_L4C, TRACE_L4D, TRACE_L01]:
        raise EchecOracle(f"coquille GUI : fichier {em.journal_fichier!r} != "
                          f"[L00, L02, L4C, L4D, L01] (ordre démarrage/WM_CREATE/"
                          f"WM_SIZE diagnostics/fenêtre — D37)")
    if em.journal != ECRAN_DEMARRAGE:
        raise EchecOracle(f"coquille GUI : ÉCRAN {em.journal!r} != {ECRAN_DEMARRAGE!r} "
                          f"— le miroir D37 n'a pas reçu les lignes de démarrage")
    if len(em.messageboxes) != 0:
        raise EchecOracle("coquille GUI : MessageBoxW inattendue")
    # clic unique (Q3) : thread scénario lancé une fois, second clic ignoré
    hwnd_p = em.qword(L.HWND_PRINCIPAL)
    em.appeler(RVA_WIN["win-04"], (hwnd_p, 0x111, 1, 0))
    if em.qword(L.DRAPEAU_WORKER) != 1 or em.threads != [(IMAGE + RVA_WIN["win-09"], 0)]:
        raise EchecOracle(f"clic : drapeau/threads {em.threads} — spawn scénario attendu")
    if (hwnd_b, 0) not in em.enablewindows:
        raise EchecOracle("clic : bouton non désactivé (EnableWindow FALSE, Q3)")
    em.appeler(RVA_WIN["win-04"], (hwnd_p, 0x111, 1, 0))
    if len(em.threads) != 1:
        raise EchecOracle("clic : second WM_COMMAND a relancé le scénario (Q3)")
    if em.journal_fichier != [TRACE_L00, TRACE_L02, TRACE_L4C, TRACE_L4D,
                              TRACE_L01, TRACE_L03]:
        raise EchecOracle(f"clic : trace L03 absente du fichier ({em.journal_fichier!r})")
    if em.journal != ECRAN_DEMARRAGE + [L.CHAINES_ASCII["L03"][1].decode("ascii") + "\r\n"]:
        raise EchecOracle(f"clic : ÉCRAN {em.journal!r} — L03 absente du miroir (D37)")
    verdicts["d40001"] = {"cas": 4, "detail": "entrée -> fenêtre -> WM_CREATE/WM_SIZE "
                                              "réels -> boucle -> sortie 0"}
    verdicts["d40002"] = {"cas": 2, "detail": "classe validée + fenêtre + traces "
                                              "L00/L01 (V2)"}
    verdicts["d40004"] = {"cas": 5, "detail": "contrôles + géométrie 764/504 (V3), "
                                              "police, clic unique, L02/L03"}
    verdicts["d40003"] = {"cas": 1, "detail": "boucle drainée, WM_QUIT -> sortie 0"}
    total += 12

    # --- échec piloté : RegisterClassExW = 0 -> MessageBoxW + LKO gle + sortie 1
    em = Emulateur(exe)
    em.installer_shims()
    em.retour_register = 0
    em.gle = 87                                     # ERROR_INVALID_PARAMETER
    em.appeler(RVA_WIN["win-01"])
    if em.code_sortie != 1 or len(em.messageboxes) != 1:
        raise EchecOracle("échec GUI : sortie/MessageBoxW attendues (E1 win-02)")
    attendu_ko = [TRACE_L00, L.CHAINES_ASCII["LKO_GUI"][1] + b"87\r\n"]
    if em.journal_fichier != attendu_ko:
        raise EchecOracle(f"échec GUI : fichier {em.journal_fichier!r} != {attendu_ko!r}")
    total += 2

    # --- win-09 : scénario complet (serveur simulé prêt, patch RÉEL) ---
    # HWND_JOURNAL factice : sur le terrain le scénario tourne TOUJOURS avec le
    # GUI vivant (lancé par le clic) — le miroir D37 doit vivre (garde E1 franchie)
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    em.uc.mem_write(IMAGE + L.DRAPEAU_SRV, struct.pack("<Q", 1))
    em.uc.mem_write(IMAGE + L.R_LISTEN, struct.pack("<Q", FAKE_SOCK))
    em.appeler(RVA_WIN["win-09"])
    attendu = [L.CHAINES_UTF16[n][1] for n in LIGNES_NOMINALES]
    if em.journal != attendu:
        manquantes = [l for l in attendu if l not in em.journal]
        raise EchecOracle(f"win-09 : journal divergent ({len(em.journal)} lignes, "
                          f"attendu {len(attendu)}) ; manquantes : {manquantes[:3]}")
    if em.journal_fichier != [latin1(t) for t in attendu]:
        raise EchecOracle("win-09 : journal fichier != miroir Latin-1 des 11 lignes")
    if em.qword(L.R_ETAT_PATCH) != 0:
        raise EchecOracle("win-09 : état patch final != 0 (rollback incomplet)")
    octets_entree = bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8))
    if octets_entree != exe[L.TEXT2_FILE + (L.ECHO_ENTREE - L.TEXT2_RVA):][:8]:
        raise EchecOracle("win-09 : entrée écho non restaurée après rollback")
    if em.qword(L.R_QUIT) != 1 or len(em.fermetures) < 2:
        raise EchecOracle("win-09 : arrêt propre absent (Q4)")
    if len(em.envois) != 3 or any(e != L.PHRASE for e in em.envois):
        raise EchecOracle("win-09 : émissions inattendues (I2 de win-10)")
    verdicts["d40009"] = {"cas": 5, "detail": "journal écran exact (11 lignes) + "
                                              "fichier miroir, rollback, arrêt, 3 échanges"}
    verdicts["d40010"] = {"cas": 3, "detail": "échanges vérifiés identité/MAJUSCULES/identité"}
    verdicts["c30007"] = {"cas": 3, "detail": "bascule+effet+rollback réels (héritage)"}
    total += 11

    # --- falsification : octets corrompus -> porte R10 détecte tout (zéro silence)
    detectees = 0
    cibles = _blocs() + [("c30014", L.R_STAGING)]
    for bid, rva in cibles:
        for offset in (11, 23):
            mutant = bytearray(exe)
            mutant[_fichier_rva(rva) + offset] ^= 0xFF
            try:
                em2 = Emulateur(bytes(mutant))
                em2.installer_shims()
                r2 = em2.appeler(RVA_WIN["win-06"])
            except Exception:
                detectees += 1         # exécution dérivée (UcError...) = détection
                break
            if r2 == 4:
                if offset == 23:
                    raise EchecOracle(f"falsification : {bid} (octet {offset}) "
                                      f"non détecté — oracle vide")
                continue                      # tenter le second offset
            detectees += 1
            break
        else:
            raise EchecOracle(f"falsification : {bid} non détecté")
    falsification = f"{detectees}/{len(cibles)} blocs détectés (octets 11/23)"
    total += detectees

    # --- falsification RECT (V4 win-04:R2) : 0x28 -> 0x24 = le défaut D36 ---
    motif = bytes.fromhex("448b5424")           # mov r10d, dword ptr [rsp + ??]
    base_fichier = _fichier_rva(RVA_WIN["win-04"])
    tranche = exe[base_fichier:base_fichier + 0x380]
    pos = tranche.find(motif + b"\x28")
    if pos < 0:
        raise EchecOracle("falsification RECT : lecture RECT.right introuvable "
                          "(motif 44 8B 54 24 28 absent de win-04)")
    mutant = bytearray(exe)
    mutant[base_fichier + pos + 4] = 0x24       # le défaut originel : RECT.top
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    try:
        em.appeler(RVA_WIN["win-01"])
        raise EchecOracle("falsification RECT : coquille GUI VERTE avec RECT.top "
                          "— l'invariant géométrique n'a pas fonctionné (V4)")
    except EchecOracle as exc:
        if "géométrie invalide" not in str(exc):
            raise
    total += 1

    # --- falsification D37 (anti-régression miroir) : re-cibler la trace L01
    # de win-02 vers win-11 en direct (le défaut demo.2 : fichier seul, écran
    # muet) → la coquille GUI doit ÉCHOUER sur le contrôle écran ---
    base02 = _fichier_rva(RVA_WIN["win-02"])
    tranche02 = exe[base02:base02 + 0x180]
    cibles = []
    for i in range(len(tranche02) - 5):
        if tranche02[i] == 0xE8:
            disp = struct.unpack_from("<i", tranche02, i + 1)[0]
            if RVA_WIN["win-02"] + i + 5 + disp == L.JOURNAL_TRACE:
                cibles.append(i)
    if len(cibles) != 3:
        raise EchecOracle(f"falsification D37 : {len(cibles)} appels trace dans "
                          f"win-02 (attendu 3 : L00/L01/LKO)")
    mutant = bytearray(exe)
    i_l01 = cibles[1]                        # le 2e appel = trace L01
    disp = RVA_WIN["win-11"] - (RVA_WIN["win-02"] + i_l01 + 5)
    struct.pack_into("<i", mutant, base02 + i_l01 + 1, disp)
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    # le contrôle écran est INLINE ici (les vérifications de la coquille vivent
    # dans executer(), pas dans appeler() — la falsification RECT, elle, est
    # détectée par un shim PENDANT l'exécution)
    em.appeler(RVA_WIN["win-01"])
    if em.journal == ECRAN_DEMARRAGE:
        raise EchecOracle("falsification D37 : l'ÉCRAN a tout reçu malgré L01 "
                          "re-ciblée vers win-11 — l'anti-régression ne garde "
                          "rien (V4 win-02:R3) : le défaut demo.2 (écran muet) "
                          "serait réintroduisible en silence")
    if em.journal_fichier != [TRACE_L00, TRACE_L02, TRACE_L4C, TRACE_L4D, TRACE_L01]:
        raise EchecOracle(f"falsification D37 : fichier altéré {em.journal_fichier!r} "
                          "— la mutation devait être chirurgicale (L01 au fichier, "
                          "absente de l'écran uniquement)")
    total += 1

    empreinte = hashlib.sha256(
        json.dumps({k: v for k, v in verdicts.items()}, sort_keys=True).encode("ascii")
        + f"|graine={graine}".encode("ascii")).hexdigest()
    return {"total_cas": total, "blocs": verdicts, "falsification": falsification,
            "empreinte": "sha256:" + empreinte, "graine": graine}
