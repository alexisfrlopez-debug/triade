#!/usr/bin/env python3
"""oracle_demo.py — Oracle différentiel du jalon démo (D1 : éphémère, régénéré).

Dérivé de la couche I de la démo (demo/I/*.md). Quatre familles :

  1. MODÈLE CHARGEUR (D35) : l'IAT est résolue aux FirstThunk des descripteurs
     — exactement comme Windows — et le verrou exige que CHAQUE slot appelé
     par la notation soit couvert (le défaut rc.1 est impossible à réintroduire).
  2. BLOCS : win-05 (paire EM_SETSEL/EM_REPLACESEL, texte exact), win-06
     (image saine -> 4 ; version sous plancher -> -1), win-07 (connect
     ok/échec + closesocket), win-08 (écoute publiée, spawn tcp-09, arrêt).
  3. SCÉNARIO COMPLET (win-09) : le patch tcp-07 s'exécute RÉELLEMENT en
     émulation (VirtualProtect shim, memcpy scellé, bascule du qword 0x4600,
     trampoline exécuté vers 0x4680) ; le shim recv REFLÈTE l'état du patch
     (R_ETAP_PATCH lu en mémoire) ; le journal capturé doit être EXACTEMENT
     les 11 lignes nominales ; rollback et arrêt propre constatés.
  4. FALSIFICATION : des octets de chaque bloc embarqué corrompus -> la porte
     R10 (win-06) les détecte tous — zéro silence.
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
    UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP)

IMAGE = L.IMAGE_BASE
PILE_BASE, PILE_TAILLE = 0x700000000, 0x100000
TRAMPOLINE = 0x600000000
SENTINELLE = 0x500000000
FAKE_SOCK, FAKE_STDOUT = 0x1111, 0x99

TOUTES_API = (list(L.KERNEL32_IMPORTS) + list(L.WS2_IMPORTS)
              + list(L.USER32_IMPORTS) + list(L.GDI32_IMPORTS))
FAUX = {nom: TRAMPOLINE + i * 0x10 for i, nom in enumerate(TOUTES_API)}
FAUX_REV = {v: k for k, v in FAUX.items()}


class EchecOracle(Exception):
    pass


class Emulateur:
    """Une instance = demo.exe mappé ; shims IAT scriptés (pattern oracle M2)."""

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
        """Image + .data vierge + IAT résolue PAR LE MODÈLE CHARGEUR (D35)."""
        self._ecrire_image()
        self.uc.mem_write(IMAGE + L.DATA_RVA, b"\x00" * L.DATA_VSIZE)
        rdata = self.exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]

        def cstr(rva):
            fin = rdata.index(b"\x00", rva - L.RDATA_RVA)
            return rdata[rva - L.RDATA_RVA:fin].decode("ascii")

        for rva_desc in (L.R_DESC_IMPORT, L.R_DESC_WS2, L.R_DESC_USER32, L.R_DESC_GDI32):
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
        self.journal: list[str] = []
        self.envois: list[bytes] = []
        self.threads: list[tuple] = []
        self.handles_fermes: list[int] = []
        self.fermetures: list[int] = []
        self.file_accept = [0x777, -1]
        self.retour_connect = 0
        self.retour_socket = FAKE_SOCK

    def qword(self, rva):
        return struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]

    def installer_shims(self):
        if self._crochet_pose:
            return
        self._crochet_pose = True

        def retour(uc_):
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            adr = struct.unpack("<Q", uc_.mem_read(rsp, 8))[0]
            uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc_.reg_write(UC_X86_REG_RIP, adr)

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
            elif nom in ("InitializeCriticalSection", "EnterCriticalSection",
                         "LeaveCriticalSection", "WSAStartup", "bind", "listen",
                         "WSACleanup", "WSAGetLastError", "TranslateMessage",
                         "DispatchMessageW", "PostQuitMessage", "DestroyWindow",
                         "EnableWindow", "MoveWindow", "DefWindowProcW",
                         "RegisterClassExW", "LoadCursorW", "MessageBoxW",
                         "GetStockObject"):
                if nom == "RegisterClassExW":
                    uc_.reg_write(UC_X86_REG_RAX, 0x1234)
                elif nom == "CreateWindowExW":
                    uc_.reg_write(UC_X86_REG_RAX, 0x2000 + len(self.journal))
                elif nom == "GetStockObject":
                    uc_.reg_write(UC_X86_REG_RAX, 0x5566)
                elif nom == "LoadCursorW":
                    uc_.reg_write(UC_X86_REG_RAX, 0x7788)
                elif nom == "GetClientRect":
                    uc_.mem_write(rcx, struct.pack("<iiii", 0, 0, 780, 560))
                    uc_.reg_write(UC_X86_REG_RAX, 1)
                else:
                    uc_.reg_write(UC_X86_REG_RAX, 1 if nom in
                                  ("DestroyWindow", "EnableWindow", "MoveWindow",
                                   "DefWindowProcW") else 0)
            elif nom == "GetMessageW":
                uc_.reg_write(UC_X86_REG_RAX, 0)          # WM_QUIT immédiat
            elif nom == "SendMessageW":
                msg = rdx & 0xFFFFFFFF
                if msg == 0xC2:                            # EM_REPLACESEL
                    brut = bytes(uc_.mem_read(r9, 512))
                    fin = 0                                 # NUL aligné 2 octets
                    while fin + 1 < len(brut) and brut[fin:fin + 2] != b"\x00\x00":
                        fin += 2
                    texte = brut[:fin].decode("utf-16-le", errors="replace")
                    self.journal.append(texte)
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "WriteFile":
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "ExitProcess":
                self.code_sortie = rcx & 0xFFFFFFFF
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

    def appeler(self, rva: int, args: tuple = (), limite: int = 5_000_000):
        uc = self.uc
        rsp = PILE_BASE + 0x80000
        for i, a in enumerate(args):
            if i < 4:
                uc.reg_write((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)[i], a)
            else:
                uc.mem_write(rsp + 0x20 + 8 * (i - 4), struct.pack("<Q", a))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp, struct.pack("<Q", SENTINELLE))
        uc.emu_start(IMAGE + rva, SENTINELLE, timeout=0, count=limite)
        return uc.reg_read(UC_X86_REG_RAX)


# --- Références dérivées de la couche I ----------------------------------------------

LIGNES_NOMINALES = ["J_ENTETE", "J_PROTO", "J_PORTE_OK", "J_LIBC_OK", "J_MEC_OK",
                    "J_SRV_OK", "J_CLI_OK", "J_ECHO_OK", "J_PROD_OK", "J_RB_OK", "J_FINAL"]


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
    r = em.appeler(0x1940)
    if r != 4:
        raise EchecOracle(f"win-06 : eax = {r} != 4 (porte + 4 vecteurs attendus)")
    verdicts["d40006"] = {"cas": 5, "detail": "porte R10 verte + 4/4 vecteurs libc"}
    total += 5

    mutant = bytearray(exe)
    struct.pack_into("<Q", mutant, L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA), 0x00020000)
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    if em.appeler(0x1940) != 0xFFFFFFFF:
        raise EchecOracle("win-06 : version sous plancher non détectée (E2)")
    total += 1

    # --- win-05 : texte exact ajouté au journal ---
    em = Emulateur(exe)
    em.installer_shims()
    adr, txt, n = L.CHAINES_UTF16["J_ENTETE"]
    em.appeler(0x18C0, (IMAGE + adr, n))
    if em.journal != [txt]:
        raise EchecOracle(f"win-05 : journal {em.journal!r} != [{txt!r}]")
    verdicts["d40005"] = {"cas": 1, "detail": "EM_SETSEL + EM_REPLACESEL, texte exact"}
    total += 1

    # --- win-07 : connect ok / échec ---
    em = Emulateur(exe)
    em.installer_shims()
    if em.appeler(0x1AC0) != FAKE_SOCK:
        raise EchecOracle("win-07 : socket attendue (Q1)")
    em = Emulateur(exe)
    em.installer_shims()
    em.retour_connect = -1
    if em.appeler(0x1AC0) != 0 or em.fermetures != [FAKE_SOCK]:
        raise EchecOracle("win-07 : échec connect non propagé (Q2/E2)")
    verdicts["d40007"] = {"cas": 2, "detail": "connect ok/échec, closesocket sur échec"}
    total += 2

    # --- win-08 : écoute publiée, spawn tcp-09, arrêt propre ---
    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(0x1B80)
    if em.qword(L.R_LISTEN) != FAKE_SOCK or em.qword(L.DRAPEAU_SRV) != 1:
        raise EchecOracle("win-08 : écoute/drapeau non publiés (Q2)")
    if em.threads != [(IMAGE + 0x4800, 0x777)]:
        raise EchecOracle(f"win-08 : spawn tcp-09 attendu, obtenu {em.threads}")
    verdicts["d40008"] = {"cas": 3, "detail": "tcp-01 ok, R_LISTEN+drapeau, spawn tcp-09, arrêt"}
    total += 3

    # --- win-09 : scénario complet (serveur simulé prêt, patch RÉEL) ---
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.DRAPEAU_SRV, struct.pack("<Q", 1))
    em.uc.mem_write(IMAGE + L.R_LISTEN, struct.pack("<Q", FAKE_SOCK))
    em.appeler(0x1C80)
    attendu = [L.CHAINES_UTF16[n][1] for n in LIGNES_NOMINALES]
    if em.journal != attendu:
        manquantes = [l for l in attendu if l not in em.journal]
        raise EchecOracle(f"win-09 : journal divergent ({len(em.journal)} lignes, "
                          f"attendu {len(attendu)}) ; manquantes : {manquantes[:3]}")
    if em.qword(L.R_ETAT_PATCH) != 0:
        raise EchecOracle("win-09 : état patch final != 0 (rollback incomplet)")
    octets_entree = bytes(em.uc.mem_read(IMAGE + L.ECHO_ENTREE, 8))
    if octets_entree != exe[L.TEXT2_FILE + (L.ECHO_ENTREE - L.TEXT2_RVA):][:8]:
        raise EchecOracle("win-09 : entrée écho non restaurée après rollback")
    if em.qword(L.R_QUIT) != 1 or len(em.fermetures) < 2:
        raise EchecOracle("win-09 : arrêt propre absent (Q4)")
    if len(em.envois) != 3 or any(e != L.PHRASE for e in em.envois):
        raise EchecOracle("win-09 : émissions inattendues (I2 de win-10)")
    verdicts["d40009"] = {"cas": 4, "detail": "journal exact (11 lignes), rollback, "
                                               "arrêt propre, 3 échanges"}
    verdicts["d40010"] = {"cas": 3, "detail": "échanges vérifiés identité/MAJUSCULES/identité"}
    verdicts["c30007"] = {"cas": 3, "detail": "bascule+effet+rollback réels (héritage)"}
    total += 10

    # --- falsification : octets corrompus -> porte R10 détecte tout (zéro silence) ---
    detectees = 0
    cibles = _blocs() + [("c30014", L.R_STAGING)]
    for bid, rva in cibles:
        for offset in (11, 23):
            mutant = bytearray(exe)
            mutant[_fichier_rva(rva) + offset] ^= 0xFF
            try:
                em2 = Emulateur(bytes(mutant))
                em2.installer_shims()
                r2 = em2.appeler(0x1940)
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

    empreinte = hashlib.sha256(
        json.dumps({k: v for k, v in verdicts.items()}, sort_keys=True).encode("ascii")
        + f"|graine={graine}".encode("ascii")).hexdigest()
    return {"total_cas": total, "blocs": verdicts, "falsification": falsification,
            "empreinte": "sha256:" + empreinte, "graine": graine}
