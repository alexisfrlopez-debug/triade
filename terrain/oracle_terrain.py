#!/usr/bin/env python3
"""oracle_terrain.py — Oracle du jalon terrain (D48 : éphémère, régénéré).

Dérivé de la couche I du terrain (terrain/I/*.md). Sept familles :

  1. SUP-22 DIFFÉRENTIEL : 10 000 cas contraints vs référence Python — le
     balayeur est pur par contrat (I3), testable comme http-04 en M3.
  2. SUP-21 HORODATAGE : horloge fixée — nom du run et ligne S01 octet par
     octet, trois horloges (nominale, minuit, fin d'année).
  3. SUP-11 JOURNAL : 7 vecteurs win-11 transposés (modes, chemin horodaté,
     paresse, échec, re-tentative, multi-lignes, différenciation .txt).
  4. COQUILLE GUI : sup-01 depuis l'entrée — l'horodatage AVANT la fenêtre
     (ordre prouvé par la séquence des appels), classe « TRIADE_superviseur »,
     wndproc scellé 0x1640, WM_CREATE/WM_SIZE réels, géométrie, journal
     [L00, L02, L4C, L4D, L01], clic unique → spawn sup-09, L03.
  5. SCÉNARIO NOMINAL COMPLET (sup-09) : T1/T2/T3 enchaînés sur des processus
     scriptés (demo.exe 17 lignes, proxy tuyaux bannière/événements/arret,
     curl pages/OAuth/session/PUT) — journal d'or ÉCRAN + FICHIER exact,
     ordre porte→T1→T2→T3, quit écrit avant l'attente, requêtes composées
     octet par octet, nettoyage intégral, zéro secret au journal (I1).
  6. ÉCHECS PILOTÉS : RegisterClassExW=0 (sortie 1) ; démo absente ; journal
     démo non conforme (16 lignes) ; curl http code 22 ; jetons absents ;
     réponse OAuth muette — un KO n'arrête jamais les tests suivants.
  7. FALSIFICATION : la porte R10 détecte tout octet corrompu (22 blocs +
     2 zones de données, la table couvre les gabarits Drive — D48) ; cinq
     mutations ciblées (constante 17, longueur d'étiquette, ordre T1/T2/T3,
     nettoyage, quit) sont chacune attrapées par leur verrou.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import importlib.util as _ilu
if "layout_terrain" in sys.modules:
    L = sys.modules["layout_terrain"]
else:
    _spec = _ilu.spec_from_file_location("layout_terrain", os.path.join(ICI, "layout.py"))
    L = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(L)
    sys.modules["layout_terrain"] = L

from unicorn import (Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UcError,
                     UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC, UC_PROT_ALL)
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
TAMPONS = 0x520000000            # zone de test du différentiel (64 Kio)
FAKE_HANDLE_FICHIER = 0xABCD
FAKE_HWND_DEMO, FAKE_HWND_BTN_DEMO = 0x97001, 0x97002
FAKE_HPROC = 0x6001              # premier handle de processus scripté
PIPE_IN_RD, PIPE_IN_WR = 0x5001, 0x5002
PIPE_OUT_RD, PIPE_OUT_WR = 0x5003, 0x5004

TOUTES_API = (list(L.KERNEL32_IMPORTS) + list(L.KERNEL32B_IMPORTS)
              + list(L.KERNEL32C_IMPORTS) + list(L.USER32_IMPORTS)
              + list(L.USER32B_IMPORTS) + list(L.GDI32_IMPORTS))
FAUX = {nom: TRAMPOLINE + i * 0x10 for i, nom in enumerate(TOUTES_API)}
FAUX_REV = {v: k for k, v in FAUX.items()}

RVA_SUP = {spec.split(":")[0]: rva for _, spec, rva, _, _, _ in L.BLOCS_TERRAIN}

REGS_CONTEXTE = (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                 UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP, UC_X86_REG_RSP,
                 UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                 UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
                 UC_X86_REG_RIP, UC_X86_REG_EFLAGS)


class EchecOracle(Exception):
    pass


def clobber_volatils(uc_):
    """D38 (héritage) : un appel IAT détruit les registres caller-saved."""
    uc_.reg_write(UC_X86_REG_RCX, 0xCCCCCCCCCCCCCCCC)
    uc_.reg_write(UC_X86_REG_RDX, 0xCCCCCCCCCCCCCCCC)
    uc_.reg_write(UC_X86_REG_R8, 0xCCCCCCCCCCCCCCCC)
    uc_.reg_write(UC_X86_REG_R9, 0xCCCCCCCCCCCCCCCC)
    uc_.reg_write(UC_X86_REG_R10, 0)
    uc_.reg_write(UC_X86_REG_R11, 0x246)


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


# --- Le journal démo de 17 lignes (T1 : ce que demo.exe 0.3.0 écrit) --------------

def _journal_demo_17() -> list[bytes]:
    """6 lignes de démarrage (ASCII démo) + 11 lignes de preuve (Latin-1 J_*)."""
    import importlib.util as ilu
    _s = ilu.spec_from_file_location("layout_demo_j", os.path.join(
        os.path.dirname(ICI), "demo", "layout.py"))
    LD = ilu.module_from_spec(_s)
    _s.loader.exec_module(LD)
    lignes = []
    for nom in ("L00", "L02", "L4C", "L4D", "L01", "L03"):
        base = LD.CHAINES_ASCII[nom][1]
        lignes.append(base + (b"1" if nom in ("L4C", "L4D") else b"") + b"\r\n")
    for nom in ("J_ENTETE", "J_PROTO", "J_PORTE_OK", "J_LIBC_OK", "J_MEC_OK",
                "J_SRV_OK", "J_CLI_OK", "J_ECHO_OK", "J_PROD_OK", "J_RB_OK",
                "J_FINAL"):
        lignes.append(latin1(LD.CHAINES_UTF16[nom][1]))
    return lignes


JOURNAL_DEMO_17 = None   # posé à la première émulation (import démo différé)


class Emulateur:
    """Une instance = superviseur.exe mappé ; shims IAT scriptés (pattern démo).

    Le modèle chargeur (D35) résout l'IAT depuis les SIX descripteurs — les
    INT/hints de kernel32#3 et user32#2 vivent en .text2 (zone données 2),
    la porte R10 les couvre (D48). Système de fichiers virtuel pour tous les
    fichiers du terrain ; tuyaux et processus scriptés par cmdline.
    """

    def __init__(self, exe: bytes):
        self.exe = bytes(exe)
        # D50 : le modèle chargeur valide l'en-tête comme Windows — SizeOfHeaders
        # DOIT couvrir la table des sections (aligné FILE_ALIGN). terrain.2 est
        # mort de cette règle (0x238 réels pour 0x200 déclarés : lancement
        # refusé au terrain) alors que l'oracle mappait les sections par le
        # plan, aveugle à l'en-tête du fichier lui-même.
        d = self.exe
        if len(d) < 0x100 or d[:2] != b"MZ":
            raise EchecOracle("chargeur : pas un fichier PE")
        e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
        if d[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise EchecOracle("chargeur : signature PE absente")
        nb_sec, = struct.unpack_from("<H", d, e_lfanew + 6)
        taille_opt, = struct.unpack_from("<H", d, e_lfanew + 20)
        fin_reelle = e_lfanew + 4 + 20 + taille_opt + nb_sec * 40
        opt = e_lfanew + 4 + 20
        fal, = struct.unpack_from("<I", d, opt + 36)
        soh, = struct.unpack_from("<I", d, opt + 60)
        soi, = struct.unpack_from("<I", d, opt + 56)
        if soh < fin_reelle:
            raise EchecOracle(
                f"chargeur : SizeOfHeaders {soh:#x} ne couvre pas la table des "
                f"sections ({fin_reelle:#x}) — Windows refuserait l'image (D50)")
        if soh % fal:
            raise EchecOracle(f"chargeur : SizeOfHeaders {soh:#x} non aligné FILE_ALIGN")
        if soi < L.SIZE_OF_IMAGE:
            raise EchecOracle(f"chargeur : SizeOfImage {soi:#x} < plan {L.SIZE_OF_IMAGE:#x}")
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(IMAGE, L.SIZE_OF_IMAGE)
        uc.mem_map(PILE_BASE, PILE_TAILLE)
        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_map(SENTINELLE, 0x1000)
        uc.mem_map(TAMPONS, 0x10000)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)
        uc.mem_write(SENTINELLE, b"\xc3" * 0x1000)
        self._crochet_pose = False
        self.reinit()

    def _ecrire_image(self):
        uc = self.uc
        uc.mem_protect(IMAGE, L.SIZE_OF_IMAGE, UC_PROT_ALL)
        uc.mem_write(IMAGE + L.TEXT_RVA, self.exe[L.TEXT_FILE:L.TEXT_FILE + L.TEXT_VSIZE])
        uc.mem_write(IMAGE + L.RDATA_RVA, self.exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE])
        uc.mem_write(IMAGE + L.DATA_RVA, self.exe[L.DATA_FILE:L.DATA_FILE + L.DATA_RAW])
        uc.mem_write(IMAGE + L.TEXT2_RVA, self.exe[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE])
        uc.mem_write(IMAGE + L.RSRC_RVA, self.exe[L.RSRC_FILE:L.RSRC_FILE + L.RSRC_VSIZE])
        uc.mem_write(IMAGE + L.BLOB_RVA, self.exe[L.BLOB_FILE:L.BLOB_FILE + L.BLOB_VSIZE])
        uc.ctl_remove_cache(IMAGE + L.TEXT_RVA, IMAGE + L.TEXT_RVA + L.TEXT_VSIZE)
        uc.ctl_remove_cache(IMAGE + L.TEXT2_RVA, IMAGE + L.TEXT2_RVA + L.TEXT2_VSIZE)

    def reinit(self):
        """Image + .data vierge + IAT résolue PAR LE MODÈLE CHARGEUR (D35)."""
        self._ecrire_image()
        self.uc.mem_write(IMAGE + L.DATA_RVA, b"\x00" * L.DATA_VSIZE)
        image = self.exe

        def cstr(rva):
            for base_rva, base_file, taille in ((L.RDATA_RVA, L.RDATA_FILE, L.RDATA_VSIZE),
                                                (L.TEXT2_RVA, L.TEXT2_FILE, L.TEXT2_VSIZE)):
                if base_rva <= rva < base_rva + taille:
                    zone = image[base_file:base_file + taille]
                    brut = zone[rva - base_rva:]
                    return brut[:brut.find(b"\x00")].decode("ascii")
            raise EchecOracle(f"chargeur : hint hors image @{rva:#x}")

        rdata = self.exe[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]
        for rva_desc in (L.R_DESC_IMPORT, L.R_DESC_USER32, L.R_DESC_GDI32,
                         L.R_DESC_K32B, L.R_DESC_K32C, L.R_DESC_U32B):
            oft, _, _, _nom_dll, ft = struct.unpack_from(
                "<IIIII", rdata, rva_desc - L.RDATA_RVA)
            if not (oft or ft):
                continue
            i = 0
            while True:
                hint_rva = self._qword_image(oft + 8 * i)
                if hint_rva == 0:
                    break
                nom = cstr(hint_rva + 2)
                if nom not in FAUX:
                    raise EchecOracle(f"chargeur : import inconnu : {nom}")
                self.uc.mem_write(IMAGE + ft + 8 * i, struct.pack("<Q", FAUX[nom]))
                i += 1
        for nom, rva in L.IAT_SLOTS.items():          # verrou D35
            val = struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]
            if val != FAUX[nom]:
                raise EchecOracle(f"chargeur/D35 : slot {nom} @{rva:#x} non résolu "
                                  f"({val:#x}) — FirstThunk divergent")

        # état d'émulation
        self.journal: list[str] = []            # journal ÉCRAN (EM_REPLACESEL)
        self.journal_fichier: list[bytes] = []  # lignes WriteFile du journal
        self.threads: list[tuple] = []
        self.handles_fermes: list[int] = []
        self.sequence: list[tuple] = []         # ordre global des effets (V2 sup-09)
        self._seq = 0

        def seq(evenement, detail=""):
            self._seq += 1
            self.sequence.append((self._seq, evenement, detail))

        self.seq = seq
        # GUI (héritage démo D36)
        self.classes: dict[str, tuple] = {}
        self.movewindow: list[tuple] = []
        self.sendmessages: list[tuple] = []
        self.messageboxes: list[tuple] = []
        self.enablewindows: list[tuple] = []
        self.hwnd_suivant = 0x3000
        self.retour_register = 0x1234
        self.retour_createwindow = None
        self.gle = 0
        # fichiers virtuels
        self.fichiers: dict[str, bytes] = {}
        self.fichiers_ecrits: dict[str, bytes] = {}   # miroir survivant aux suppressions
        self.handles: dict[int, dict] = {}
        self.hhandle = 0x7000
        self.createfile_appels: list[str] = []
        self.suppressions: list[str] = []
        self.retour_createfile = None           # None = réel ; -1 = échec piloté
        self.echec_createfile_chemins: set = set()   # échec CIBLÉ (D49 : kit)
        self.corrompre_lecture = None           # (chemin, offset) : écart injecté à la relecture
        self.chemin_journal: str | None = None
        # tuyaux + processus
        self.flux_proxy = b""                   # octets restants au tuyau stdout
        self.pipe_visible = 0                   # octets révélés (preuve du sondage)
        self.pipe_sondages = 0
        self.stdin_proxy = b""                  # ce que nous écrivons au stdin
        self.processus: list[dict] = []
        self.hproc = FAKE_HPROC
        self.sortie_processus: dict[int, int] = {}    # handle → code de sortie
        self.echec_createprocess: list[str] = []      # cmdlines devant échouer
        self.findwindow_reponses: list[int] = []      # 0, 0, hwnd (V2 sup-33)
        self.findwindow_appels: list[str] = []
        self.sendmsgtimeout: list[tuple] = []
        self.terminates: list[int] = []
        self.attentes: list[tuple] = []
        self.sommeils = 0
        self._pipes_crees = 0
        self._codes_scriptes: list = []
        self.horloge = (2026, 10, 2, 27, 9, 30, 12, 0)   # SYSTEMTIME
        # moteur
        self.pending: list[tuple] = []
        self.pending_retour: tuple | None = None
        self.sortie = False
        self.code_sortie: int | None = None

    def _qword_image(self, rva: int) -> int:
        """Qword depuis l'image fichier — bornes EXACTES des sections (un rva
        .text2 comme 0x6490 ne doit jamais retomber dans la fenêtre .text)."""
        for base_rva, base_file, taille in ((L.RDATA_RVA, L.RDATA_FILE, L.RDATA_VSIZE),
                                            (L.TEXT2_RVA, L.TEXT2_FILE, L.TEXT2_VSIZE)):
            if base_rva <= rva < base_rva + taille:
                return struct.unpack_from("<Q", self.exe, base_file + (rva - base_rva))[0]
        raise EchecOracle(f"lecture image hors bornes @{rva:#x}")

    def qword(self, rva):
        return struct.unpack("<Q", self.uc.mem_read(IMAGE + rva, 8))[0]

    def lire_chaine(self, rva: int) -> bytes:
        brut = bytes(self.uc.mem_read(IMAGE + rva, 700))
        return brut[:brut.find(b"\x00")]

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
            clobber_volatils(uc_)

        def arg_pile(uc_, n, taille=8):
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            brut = uc_.mem_read(rsp + 0x28 + 8 * (n - 5), taille)
            return struct.unpack("<Q" if taille == 8 else "<I", brut)[0]

        def chaine_utf16(uc_, adr, maxchars=64):
            brut = bytes(uc_.mem_read(adr, 2 * maxchars))
            fin = brut.find(b"\x00\x00")
            if fin % 2:
                fin += 1
            return brut[:fin if fin >= 0 else 2 * maxchars].decode("utf-16-le")

        def chaine_ascii(uc_, adr, maxo=690):
            brut = bytes(uc_.mem_read(adr, maxo))
            return brut[:brut.find(b"\x00")].decode("ascii", errors="replace")

        def i32(v):
            return v - 0x100000000 if v & 0x80000000 else v

        em = self

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
                uc_.reg_write(UC_X86_REG_RAX, 0x99 if c == 0xFFFFFFF5 else 0x98)
            elif nom == "CloseHandle":
                em.handles_fermes.append(rcx)
                em.handles.pop(rcx, None)
                em.seq("close", hex(rcx))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "CreateThread":
                em.threads.append((r8, r9))
                uc_.reg_write(UC_X86_REG_RAX, 0x100 + 8 * len(em.threads))
            elif nom == "VirtualProtect":
                uc_.reg_write(UC_X86_REG_RAX, 1)   # aucun appelant terrain (IAT figée)
            elif nom in ("InitializeCriticalSection", "EnterCriticalSection",
                         "LeaveCriticalSection"):
                pass                                # idem : aucun appelant vivant
            elif nom == "GetLastError":
                uc_.reg_write(UC_X86_REG_RAX, em.gle & 0xFFFFFFFF)
            elif nom == "GetModuleHandleW":
                uc_.reg_write(UC_X86_REG_RAX, IMAGE)
            elif nom == "GetModuleFileNameA":
                chemin = b"C:\\sup\\superviseur.exe\x00"
                uc_.mem_write(rdx, chemin)
                uc_.reg_write(UC_X86_REG_RAX, len(chemin) - 1)
            elif nom == "GetLocalTime":
                annee, mois, jour_sem, jour, heure, minute, seconde, ms = em.horloge
                uc_.mem_write(rcx, struct.pack("<8H", annee, mois, jour_sem, jour,
                                               heure, minute, seconde, ms))
                em.seq("horloge")
            elif nom == "CreateFileA":
                chemin = chaine_ascii(uc_, rcx)
                em.createfile_appels.append(chemin)
                if em.retour_createfile == -1 or chemin in em.echec_createfile_chemins:
                    uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                    retour(uc_)
                    return
                em.hhandle += 1
                h = em.hhandle
                access = rdx & 0xFFFFFFFF
                if access & 0x80000000:            # GENERIC_READ (sup-36 .lire / relecture kit)
                    if chemin not in em.fichiers:
                        uc_.reg_write(UC_X86_REG_RAX, 0xFFFFFFFFFFFFFFFF)
                        retour(uc_)
                        return
                    if em.corrompre_lecture and em.corrompre_lecture[0] == chemin:
                        contenu = bytearray(em.fichiers[chemin])
                        contenu[em.corrompre_lecture[1]] ^= 0xFF
                        em.fichiers[chemin] = bytes(contenu)
                    em.handles[h] = {"type": "lire", "chemin": chemin, "pos": 0}
                elif access & 4:                   # FILE_APPEND_DATA (sup-11)
                    em.handles[h] = {"type": "append", "chemin": chemin}
                    em.chemin_journal = chemin
                    em.fichiers.setdefault(chemin, b"")
                else:                              # GENERIC_WRITE (sup-36 .ecrire)
                    em.handles[h] = {"type": "ecrire", "chemin": chemin}
                    em.fichiers[chemin] = b""      # CREATE_ALWAYS tronque
                uc_.reg_write(UC_X86_REG_RAX, h)
            elif nom == "ReadFile":
                if rcx == PIPE_OUT_RD:
                    n = r8 & 0xFFFFFFFF
                    servi = em.flux_proxy[:n]
                    uc_.mem_write(rdx, servi)
                    em.flux_proxy = em.flux_proxy[n:]
                    em.pipe_sondages = 0          # chaque .attendre re-prouve le sondage
                    uc_.mem_write(r9, struct.pack("<Q", len(servi)))
                    uc_.reg_write(UC_X86_REG_RAX, 1)
                else:
                    h = em.handles.get(rcx)
                    if h and h["type"] == "lire":
                        contenu = em.fichiers.get(h["chemin"], b"")
                        n = r8 & 0xFFFFFFFF
                        servi = contenu[h["pos"]:h["pos"] + n]
                        uc_.mem_write(rdx, servi)
                        h["pos"] += len(servi)
                        uc_.mem_write(r9, struct.pack("<Q", len(servi)))
                        uc_.reg_write(UC_X86_REG_RAX, 1)
                    else:
                        uc_.reg_write(UC_X86_REG_RAX, 0)
            elif nom == "WriteFile":
                n = r8 & 0xFFFFFFFF
                donnees = bytes(uc_.mem_read(rdx, n))
                if rcx == PIPE_IN_WR:
                    em.stdin_proxy += donnees
                    em.seq("stdin", donnees.decode("ascii", errors="replace"))
                    uc_.mem_write(r9, struct.pack("<Q", n))
                    uc_.reg_write(UC_X86_REG_RAX, 1)
                else:
                    h = em.handles.get(rcx)
                    if h and h["type"] == "append":
                        em.journal_fichier.append(donnees)
                        em.fichiers[h["chemin"]] = em.fichiers.get(h["chemin"], b"") + donnees
                        uc_.mem_write(r9, struct.pack("<Q", n))
                        uc_.reg_write(UC_X86_REG_RAX, 1)
                    elif h and h["type"] == "ecrire":
                        em.fichiers[h["chemin"]] = em.fichiers.get(h["chemin"], b"") + donnees
                        em.fichiers_ecrits[h["chemin"]] = em.fichiers[h["chemin"]]
                        uc_.mem_write(r9, struct.pack("<Q", n))
                        uc_.reg_write(UC_X86_REG_RAX, 1)
                    else:
                        uc_.reg_write(UC_X86_REG_RAX, 0)
            elif nom == "FlushFileBuffers":
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "DeleteFileA":
                chemin = chaine_ascii(uc_, rcx)
                em.suppressions.append(chemin)
                em.seq("delete", chemin)
                present = chemin in em.fichiers
                em.fichiers.pop(chemin, None)
                uc_.reg_write(UC_X86_REG_RAX, 1 if present else 0)
            elif nom == "CreatePipe":
                # paires dans l'ordre : 1re = stdin (IN), 2e = stdout (OUT)
                em._pipes_crees += 1
                if em._pipes_crees == 1:
                    uc_.mem_write(rcx, struct.pack("<Q", PIPE_IN_RD))
                    uc_.mem_write(rdx, struct.pack("<Q", PIPE_IN_WR))
                else:
                    uc_.mem_write(rcx, struct.pack("<Q", PIPE_OUT_RD))
                    uc_.mem_write(rdx, struct.pack("<Q", PIPE_OUT_WR))
                em.seq("pipe")
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "CreateProcessA":
                cmdline = chaine_ascii(uc_, rdx)
                herite = arg_pile(uc_, 5, 4)
                cwd_ptr = arg_pile(uc_, 8)
                si_ptr = arg_pile(uc_, 9)
                pi_ptr = arg_pile(uc_, 10)
                si_flags = struct.unpack_from("<I", uc_.mem_read(si_ptr + 60, 4))[0]
                cwd = chaine_ascii(uc_, cwd_ptr) if cwd_ptr else ""
                em.processus.append({"cmdline": cmdline, "herite": herite,
                                     "cwd": cwd, "si_flags": si_flags})
                em.seq("spawn", cmdline[:40])
                if any(cmdline.startswith(p) for p in em.echec_createprocess):
                    uc_.reg_write(UC_X86_REG_RAX, 0)
                    retour(uc_)
                    return
                em.hproc += 1
                h = em.hproc
                code = em._code_sortie_cmdline(cmdline)
                em.sortie_processus[h] = code
                em.processus[-1]["hproc"] = h
                uc_.mem_write(pi_ptr, struct.pack("<QQII", h, h + 0x100000,
                                                  4242 + len(em.processus), 0))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "WaitForSingleObject":
                em.attentes.append((rcx, rdx & 0xFFFFFFFF))
                em.seq("attente", hex(rcx))
                uc_.reg_write(UC_X86_REG_RAX, 0)   # WAIT_OBJECT_0
            elif nom == "GetExitCodeProcess":
                code = em.sortie_processus.get(rcx, 0)
                uc_.mem_write(rdx, struct.pack("<I", code & 0xFFFFFFFF))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "TerminateProcess":
                em.terminates.append(rcx)
                em.seq("terminate", hex(rcx))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "Sleep":
                em.sommeils += 1
            elif nom == "PeekNamedPipe":
                if rcx == PIPE_OUT_RD:
                    em.pipe_sondages += 1
                    visible = len(em.flux_proxy) if em.pipe_sondages >= 3 else 0
                    uc_.mem_write(arg_pile(uc_, 5), struct.pack("<Q", visible))
                    uc_.reg_write(UC_X86_REG_RAX, 1)
                else:
                    uc_.reg_write(UC_X86_REG_RAX, 0)
            elif nom == "FindWindowW":
                nom_fen = chaine_utf16(uc_, rdx) if rdx else ""
                em.findwindow_appels.append(nom_fen)
                if em.findwindow_reponses:
                    r = em.findwindow_reponses.pop(0)
                else:
                    r = FAKE_HWND_DEMO
                uc_.reg_write(UC_X86_REG_RAX, r)
            elif nom == "FindWindowExW":
                uc_.reg_write(UC_X86_REG_RAX, FAKE_HWND_BTN_DEMO)
            elif nom == "SendMessageTimeoutW":
                msg = rdx & 0xFFFFFFFF
                em.sendmsgtimeout.append((rcx, msg))
                em.seq("sendmsg", f"hwnd={rcx:#x} msg={msg:#x}")
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "LoadCursorW":
                uc_.reg_write(UC_X86_REG_RAX, 0x7788)
            elif nom == "GetStockObject":
                uc_.reg_write(UC_X86_REG_RAX, 0x5566)
            elif nom == "GetClientRect":
                uc_.mem_write(rdx, struct.pack("<iiii", 0, 0, 780, 560))
                uc_.reg_write(UC_X86_REG_RAX, 1)
            elif nom == "RegisterClassExW":
                cbsize, _style = struct.unpack_from("<II", uc_.mem_read(rcx, 16))
                wndproc, = struct.unpack_from("<Q", uc_.mem_read(rcx + 8, 8))
                nom_classe = chaine_utf16(uc_, struct.unpack_from(
                    "<Q", uc_.mem_read(rcx + 64, 8))[0])
                if cbsize != 0x50 or not (IMAGE <= wndproc < IMAGE + L.SIZE_OF_IMAGE) \
                        or self.retour_register == 0:
                    uc_.reg_write(UC_X86_REG_RAX, 0)
                else:
                    self.classes[nom_classe] = (wndproc, 0)
                    self.seq("classe", nom_classe)
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
            elif nom in ("TranslateMessage", "DispatchMessageW", "PostQuitMessage",
                         "DestroyWindow", "DefWindowProcW", "EnableWindow"):
                if nom == "EnableWindow":
                    self.enablewindows.append((rcx, rdx & 0xFFFFFFFF))
                uc_.reg_write(UC_X86_REG_RAX, 1 if nom in
                              ("DestroyWindow", "DefWindowProcW", "EnableWindow") else 0)
            else:
                raise EchecOracle(f"shim non implémenté : {nom}")
            retour(uc_)

        self.uc.hook_add(UC_HOOK_CODE, crochet, begin=TRAMPOLINE, end=TRAMPOLINE + 0x1000)

    def _code_sortie_cmdline(self, cmdline: str) -> int:
        for attendue, code in self._codes_scriptes:
            if cmdline == attendue:
                return code
        return 0

    def scripter_sorties(self, paires: list):
        self._codes_scriptes = paires

    # --- moteur d'exécution (pilotage des appels imbriqués, héritage D36) ------

    def _sauver_contexte(self):
        return {r: self.uc.reg_read(r) for r in REGS_CONTEXTE}

    def _restaurer_contexte(self, ctx):
        for r, v in ctx.items():
            self.uc.reg_write(r, v)

    def appeler(self, rva: int, args: tuple = (), limite: int = 8_000_000,
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
                # ABI réelle : le callee lit arg5 à [entrée + 0x28] (le vrai
                # appel pousse l'adresse de retour — sup-22, premier bloc de
                # la lignée à lire ses args 5+ depuis la pile, l'exige)
                uc.mem_write(rsp + 0x28 + 8 * (i - 4), struct.pack("<Q", a))
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
                clobber_volatils(uc)    # retour d'API simulé
                debut = retadr
                continue
            debut = rip                                   # budget de pas épuisé
        return uc.reg_read(UC_X86_REG_RAX)


# =============================================================================
# Références dérivées de la couche I (aucun octet codé en dur hors du plan)
# =============================================================================

S = lambda n: L.CHAINES_SUP[n][1]          # octets .rdata zone sup
CH = L.CHAINES_ASCII

TRACE_L00 = CH["L00"][1] + b"\r\n"
TRACE_L01 = CH["L01"][1] + b"\r\n"
TRACE_L02 = CH["L02"][1] + b"\r\n"
TRACE_L03 = CH["L03"][1] + b"\r\n"
TRACE_L4C = CH["L4C"][1] + b"1\r\n"
TRACE_L4D = CH["L4D"][1] + b"1\r\n"
ECRAN_DEMARRAGE = [l.decode("ascii") for l in (TRACE_L02, TRACE_L4C, TRACE_L4D, TRACE_L01)]
FAKE_HWND_EDIT = 0x9988

HORLOGE_NOMINALE = (2026, 10, 2, 27, 9, 30, 12, 0)
NOM_RUN = b"terrain_20261027_093012.txt"
LIGNE_S01 = b"S01 date 20261027_093012"

# --- T2 : flux du proxy (bannière 40 o + événements 35/43 o + arret 7 o) --------
BANNIERE = S("FIX_BANNIERE")                       # 40 octets avec CRLF
EVT_HTTP = S("FIX_EVT_HTTP")                       # 35 octets
EVT_HTTPS = S("FIX_EVT_HTTPS")                     # 43 octets
ARRET = S("FIX_ARRET")                             # 7 octets
PAGE_HTTP, PAGE_HTTPS = b"<html>" + b"A" * 1262 + b"</html>", b"<html>" + b"B" * 1250 + b"</html>"

# --- T3 : jetons et réponses réalistes (fausses valeurs de test) ----------------
JETONS = (b"client-id-test.apps.googleusercontent.com\x00"
          b"GOCSPX-test-secret-456\x00"
          b"//test-refresh-token-789\x00"
          b"https://oauth2.googleapis.com/token\x00")
JETON_OAUTH = b"ya29.test-jeton-superviseur-terrain-0123456789"
REPONSE_OAUTH = (b'{"access_token":"' + JETON_OAUTH +
                 b'","expires_in":3600,"token_type":"Bearer"}')
URL_SESSION = (b"https://www.googleapis.com/upload/drive/v3/files"
               b"?uploadType=resumable&upload_id=ABCdef123456")
REPONSE_SESSION = (b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nLocation: "
                   + URL_SESSION + b"\r\nX-Goog-Upload-Status: active\r\n\r\n")
CHEMIN_JOURNAL = b"C:\\sup\\" + NOM_RUN
REQ_OAUTH_ATTENDUE = (b"client_id=client-id-test.apps.googleusercontent.com"
                      b"&client_secret=GOCSPX-test-secret-456"
                      b"&refresh_token=//test-refresh-token-789"
                      b"&grant_type=refresh_token")
META_ATTENDUE = (b'{"name":"' + NOM_RUN + b'","parents":["'
                 + S("DOSSIER_TEST").rstrip(b"\x00") + b'"]}')


def _cmd(nom: str) -> str:
    return L.CHAINES_SUP[nom][1].rstrip(b"\x00").decode("ascii")


CMD_JETON_ATTENDU = ("curl.exe -s --fail --max-time 30 -o terrain_jeton.json "
                     "--data @terrain_req.txt https://oauth2.googleapis.com/token")
CMD_SESSION_ATTENDU = ("curl.exe -s --fail --max-time 30 -o NUL -D terrain_session.txt "
                       "-X POST -H \"Content-Type: application/json\" "
                       "-H \"Authorization: Bearer " + JETON_OAUTH.decode() + "\" "
                       "--data @terrain_meta.json "
                       "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable")
CMD_PUT_ATTENDU = ("curl.exe -s --fail --max-time 120 -o NUL -X PUT --data-binary @"
                   + CHEMIN_JOURNAL.decode() + " " + URL_SESSION.decode())


def variante_livraison(exe: bytes, jetons: bytes | None = None) -> bytes:
    """Image de test « livraison » (D49) : l'emplacement annexe reçoit des
    jetons FICTIFS (jamais les vrais) — le slot est hors table R10, la porte
    reste verte par construction ; l'émulation prouve le chemin complet T3
    sans jamais toucher un vrai secret."""
    if jetons is None:
        jetons = JETONS
    img = bytearray(exe)
    off = L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA)
    struct.pack_into("<Q", img, off, len(jetons))
    img[off + 8: off + 8 + len(jetons)] = jetons
    return bytes(img)


def lignes_journal_or(demo17: list[bytes], livraison: bool = True) -> list[bytes]:
    """Journal d'or nominal — chaque entrée SANS le CRLF (posé par win-05/11).
    livraison : True = annexe intégrée (T3 vivant) ; False = variante publique
    du dépôt (S06B, T3 non applicable, non compté — D49)."""
    lignes = [
        S("S00"), LIGNE_S01, S("S02A"), S("S03A"),
        # kit embarqué (D49)
        S("S04A"), S("S04C"), S("S05A"), S("S05C"),
        S("S06A") if livraison else S("S06B"),
        # T1
        S("S10"), S("S11A"), S("S12A"),
        S("S13") + b"0", S("S14") + b"17",
        *[l.rstrip(b"\r\n") for l in demo17],
        S("S15A"), S("S16A"),
        # T2
        S("S20"), S("S21A"), BANNIERE.rstrip(b"\r\n"),
        # le compteur d'octets plafonne à MAX_LECTURE (sup-36 : une lecture,
        # 640 o max) — la preuve de réception, pas une mesure exhaustive
        S("S22A") + b"0", S("S23") + str(min(len(PAGE_HTTP), L.MAX_LECTURE)).encode(),
        S("FIX_EVT_HTTP").split(b"\r\n")[0], S("FIX_EVT_HTTP").split(b"\r\n")[1],
        S("S24") + b"0", S("S25") + str(min(len(PAGE_HTTPS), L.MAX_LECTURE)).encode(),
        *[l for l in S("FIX_EVT_HTTPS").split(b"\r\n") if l],
        S("FIX_ARRET").rstrip(b"\r\n"),
        S("S26") + b"7", S("S27A"), S("S28A"),
    ]
    if livraison:
        lignes += [S("S30"), S("S32"), S("S33A"), S("S34A"), S("S35A"), S("S36A")]
    lignes += [S("S07A"), S("S90")]
    return lignes


def preparer_scenario(em: Emulateur, demo17: list[bytes],
                      code_curl_http: int = 0,
                      reponse_oauth: bytes | None = REPONSE_OAUTH):
    """Pose l'état scripté du run nominal (ou dégradé) : FS + tuyaux + sorties.
    Les jetons ne sont PLUS posés au FS (D49) : ils vivent dans le slot .blob
    de la variante livraison — sup-37 les pose lui-même pendant le run."""
    global JOURNAL_DEMO_17
    em.fichiers["C:\\sup\\demo_journal.txt"] = b"".join(demo17)
    em.flux_proxy = BANNIERE + EVT_HTTP + EVT_HTTPS + ARRET
    em.pipe_sondages = 0
    # fenêtre démo trouvée au 3e sondage (V2 sup-33) ; jeton/session servis par
    # les curls scriptés via fichiers de sortie
    em.findwindow_reponses = [0, 0, FAKE_HWND_DEMO]
    em.scripter_sorties([("demo.exe", 0), ("proxy.exe", 0),
                         (_cmd("CMD_CURL_HTTP"), code_curl_http),
                         (_cmd("CMD_CURL_HTTPS"), 0),
                         (CMD_JETON_ATTENDU, 0 if reponse_oauth is not None else 22),
                         (CMD_SESSION_ATTENDU, 0 if reponse_oauth is not None else 22),
                         (CMD_PUT_ATTENDU, 0)])
    # effets de bord des curls scriptés (fichiers -o / -D)
    if code_curl_http == 0:
        em.fichiers["C:\\sup\\terrain_page_http.txt"] = PAGE_HTTP
    em.fichiers["C:\\sup\\terrain_page_https.txt"] = PAGE_HTTPS
    if reponse_oauth is not None:
        em.fichiers["C:\\sup\\terrain_jeton.json"] = reponse_oauth
        em.fichiers["C:\\sup\\terrain_session.txt"] = REPONSE_SESSION
    # TAMPON_NOM/TAMPON_AFF posés comme sup-01 l'aurait fait
    em.uc.mem_write(IMAGE + L.TAMPON_NOM, NOM_RUN + b"\x00")
    em.uc.mem_write(IMAGE + L.TAMPON_AFF, LIGNE_S01)


def _fichier_rva(rva: int) -> int:
    if rva >= L.BLOB_RVA:
        return L.BLOB_FILE + (rva - L.BLOB_RVA)
    if rva >= L.RSRC_RVA:
        return L.RSRC_FILE + (rva - L.RSRC_RVA)
    if rva >= L.TEXT2_RVA:
        return L.TEXT2_FILE + (rva - L.TEXT2_RVA)
    if rva >= L.DATA_RVA:
        return L.DATA_FILE + (rva - L.DATA_RVA)
    if rva >= L.RDATA_RVA:
        return L.RDATA_FILE + (rva - L.RDATA_RVA)
    return L.TEXT_FILE + (rva - L.TEXT_RVA)


def _blocs_terrain():
    return [(bid, rva) for bid, _, rva, _slot, _, _ in L.BLOCS_TERRAIN]


def _comparer_journal(em, lignes_or: list[bytes], contexte: str):
    attendu_fichier = [l + b"\r\n" for l in lignes_or]
    if em.journal_fichier != attendu_fichier:
        manquantes = [l for l in attendu_fichier if l not in em.journal_fichier]
        extra = [l for l in em.journal_fichier if l not in attendu_fichier]
        raise EchecOracle(f"{contexte} : journal fichier divergent "
                          f"({len(em.journal_fichier)} lignes, attendu "
                          f"{len(attendu_fichier)}) ; manquantes {manquantes[:3]!r} ; "
                          f"en trop {extra[:3]!r}")
    attendu_ecran = [l.decode("latin-1") + "\r\n" for l in lignes_or]
    if em.journal != attendu_ecran:
        raise EchecOracle(f"{contexte} : journal ÉCRAN divergent "
                          f"({len(em.journal)} lignes, attendu {len(attendu_ecran)}) — "
                          f"le miroir win-05 a perdu des lignes")


# =============================================================================
# Familles de tests
# =============================================================================

def _reference_balaye(tampon: bytes, etiquette: bytes, arret: int, cap: int):
    """Référence Python du balayeur (sup-22) : (valeur+NUL, rax)."""
    idx = tampon.find(etiquette)
    if idx < 0:
        return None, 0                    # absent : destination INTACTE
    valeur = tampon[idx + len(etiquette):]
    fin = valeur.find(bytes([arret]))
    if fin >= 0:
        valeur = valeur[:fin]
    if len(valeur) >= cap:                # tronqué : max-1 octets + NUL, rax = 0
        return valeur[:cap - 1] + b"\x00", 0
    return valeur + b"\x00", len(valeur)


def test_differentiel_balaye(exe: bytes, graine: int):
    """Famille 1 : sup-22 — 10 000 cas contraints vs référence Python."""
    rng = random.Random(graine)
    em = Emulateur(exe)
    em.installer_shims()
    BALAYEUR = RVA_SUP["sup-22"]
    BUFS, ETIQ, DEST = TAMPONS + 0x1000, TAMPONS + 0x3000, TAMPONS + 0x5000
    cas = 0
    for _ in range(10_000):
        n = rng.randint(0, 200)
        etiquette = bytes(rng.choice(b"abcdefghXYZ\"\\/: ") for _ in range(rng.randint(1, 16)))
        arret = rng.choice([ord('"'), 0x0D, ord(":")])
        tampon = bytearray(bytes(rng.choice(b"abcdefghXYZ\"\\/: .,=0123456789")
                                 for _ in range(n)))
        scenario = rng.randint(0, 5)
        if scenario == 1 and n >= len(etiquette):            # étiquette présente
            pos = rng.randint(0, n - len(etiquette))
            tampon[pos:pos + len(etiquette)] = etiquette
        elif scenario == 2 and n >= len(etiquette):          # collée à la fin
            tampon = bytearray(etiquette + bytes(tampon[:n - len(etiquette)]))
        elif scenario == 3 and n >= len(etiquette) + 2:      # valeur vide (arrêt direct)
            pos = rng.randint(0, n - len(etiquette) - 1)
            tampon[pos:pos + len(etiquette)] = etiquette + bytes([arret])
        cap = rng.randint(1, 64)
        tampon = bytes(tampon)
        em.uc.mem_write(BUFS, tampon + b"\x00")
        em.uc.mem_write(ETIQ, etiquette + b"\x00")
        em.uc.mem_write(DEST, b"\xAA" * 128)
        rax = em.appeler(BALAYEUR, (BUFS, len(tampon), ETIQ, len(etiquette),
                                    arret, DEST, cap))
        ref_valeur, ref_rax = _reference_balaye(tampon, etiquette, arret, cap)
        cas += 1
        if rax != ref_rax:
            raise EchecOracle(f"sup-22 différentiel cas {cas} : rax {rax} != "
                              f"{ref_rax} (tampon {tampon!r} étiquette {etiquette!r} "
                              f"arrêt {arret:#x} cap {cap})")
        pose = bytes(em.uc.mem_read(DEST, 128))
        if ref_valeur is None:
            if pose != b"\xAA" * 128:
                raise EchecOracle(f"sup-22 cas {cas} : absent mais destination "
                                  f"modifiée ({pose[:16]!r}) — I1 violé")
        elif pose[:len(ref_valeur)] != ref_valeur:
            raise EchecOracle(f"sup-22 cas {cas} : valeur {pose[:len(ref_valeur)]!r} "
                              f"!= {ref_valeur!r} (Q3/Q5/Q6)")
    return cas


def test_horodatage(exe: bytes):
    """Famille 2 : sup-21 — trois horloges, nom et ligne S01 octet par octet."""
    em = Emulateur(exe)
    em.installer_shims()
    attendus = [
        ((2026, 10, 2, 27, 9, 30, 12, 0), b"terrain_20261027_093012.txt",
         b"S01 date 20261027_093012"),
        ((2000, 1, 1, 1, 0, 0, 0, 0), b"terrain_20000101_000000.txt",
         b"S01 date 20000101_000000"),
        ((2026, 12, 4, 31, 23, 59, 59, 0), b"terrain_20261231_235959.txt",
         b"S01 date 20261231_235959"),
    ]
    cas = 0
    for horloge, nom, aff in attendus:
        em.horloge = horloge
        r = em.appeler(RVA_SUP["sup-21"])
        cas += 1
        if r != 24:
            raise EchecOracle(f"sup-21 {horloge[:4]} : rax {r} != 24 (Q4)")
        pose_nom = bytes(em.uc.mem_read(IMAGE + L.TAMPON_NOM, 32))
        if pose_nom != nom + b"\x00" + b"\x00" * (31 - len(nom)):
            raise EchecOracle(f"sup-21 : TAMPON_NOM {pose_nom[:28]!r} != {nom!r} (Q2)")
        pose_aff = bytes(em.uc.mem_read(IMAGE + L.TAMPON_AFF, 32))
        if pose_aff[:24] != aff:
            raise EchecOracle(f"sup-21 : TAMPON_AFF {pose_aff[:24]!r} != {aff!r} (Q3)")
    return cas


def test_journal_sup11(exe: bytes):
    """Famille 3 : sup-11 — les 7 vecteurs win-11 transposés au nom dynamique."""
    em = Emulateur(exe)
    em.installer_shims()
    SUP11 = RVA_SUP["sup-11"]
    # V4 paresse : aucune API fichier avant la première ligne
    if em.createfile_appels:
        raise EchecOracle("sup-11 : ouverture avant la première ligne (V4)")
    # V2 modes — TAMPON_NOM posé par sup-21 d'abord (P2)
    em.horloge = HORLOGE_NOMINALE
    em.appeler(RVA_SUP["sup-21"])
    a_l01, o_l01, _ = CH["L01"]
    r1 = em.appeler(SUP11, (IMAGE + a_l01, len(o_l01), 0, 0))
    ako, oko, _ = CH["LKO_GUI"]
    r2 = em.appeler(SUP11, (IMAGE + ako, len(oko), 1, 1400))
    attendu = [o_l01 + b"\r\n", oko + b"1400\r\n"]
    if em.journal_fichier != attendu or (r1, r2) != (1, 1):
        raise EchecOracle(f"sup-11 : modes 0/1 {em.journal_fichier!r} != {attendu!r}")
    # V3 chemin : le journal du run, JAMAIS demo_journal.txt (V7)
    chemin = em.chemin_journal
    if chemin != "C:\\sup\\terrain_20261027_093012.txt":
        raise EchecOracle(f"sup-11 : chemin {chemin!r} — attendu le nom horodaté "
                          f"du run à côté de l'exe (V3/V7)")
    if "demo_journal.txt" in (chemin or ""):
        raise EchecOracle("sup-11 : collision avec le journal de la démo (V7)")
    # V2 mode 2 + idempotence CRLF
    texte16 = "écho → —"
    utf16 = texte16.encode("utf-16-le")
    em.uc.mem_write(TAMPONS, utf16)
    em.appeler(SUP11, (TAMPONS, len(texte16), 2, 0))
    if em.journal_fichier[-1] != b"\xe9cho > -\r\n":
        raise EchecOracle(f"sup-11 : conversion mode 2 {em.journal_fichier[-1]!r} "
                          f"!= {b'\\xe9cho > -\\r\\n'!r}")
    em.appeler(SUP11, (TAMPONS, len(texte16), 2, 0))
    if em.journal_fichier[-1] != b"\xe9cho > -\r\n":
        raise EchecOracle("sup-11 : CRLF dédoublé en mode 2 (idempotence Q1)")
    # V5 échec piloté + re-tentative
    em.retour_createfile = -1
    em.uc.mem_write(IMAGE + L.R_JOURNAL_HANDLE, struct.pack("<Q", 0))
    if em.appeler(SUP11, (IMAGE + a_l01, len(o_l01), 0, 0)) != 0:
        raise EchecOracle("sup-11 : échec CreateFileA non propagé (V5)")
    if em.qword(L.R_JOURNAL_HANDLE) != 0xFFFFFFFFFFFFFFFF:
        raise EchecOracle("sup-11 : handle non marqué en échec (V5)")
    n_avant = len(em.journal_fichier)
    em.retour_createfile = None
    if em.appeler(SUP11, (IMAGE + a_l01, len(o_l01), 0, 0)) != 1 \
            or len(em.journal_fichier) != n_avant + 1:
        raise EchecOracle("sup-11 : re-tentative après échec absente (V5)")
    # V6 multi-lignes : ordre et contenu exacts
    if em.journal_fichier[:2] != attendu:
        raise EchecOracle("sup-11 : l'ordre des premières lignes a bougé (V6)")
    return 7


def test_coquille_gui(exe: bytes):
    """Famille 4 : sup-01 depuis l'entrée — horodatage AVANT fenêtre, clic unique."""
    em = Emulateur(exe)
    em.installer_shims()
    em.appeler(RVA_SUP["sup-01"])
    if em.code_sortie != 0:
        raise EchecOracle(f"coquille GUI : sortie {em.code_sortie} != 0")
    # V2 sup-01 : sup-21 AVANT sup-02 — l'horloge précède l'enregistrement de classe
    evts = em.sequence
    i_horloge = next((i for i, (_n, e, _d) in enumerate(evts) if e == "horloge"), None)
    i_classe = next((i for i, (_n, e, _d) in enumerate(evts) if e == "classe"), None)
    if i_horloge is None or i_classe is None:
        raise EchecOracle("coquille GUI : horloge/classe manquantes — sup-21 ou "
                          "sup-02 n'a pas vécu (Q1 sup-01)")
    if i_classe < i_horloge:
        raise EchecOracle("coquille GUI : la fenêtre vit avant l'horodatage — "
                          "le journal s'ouvrirait sans nom (Q1/V3 sup-01)")
    if "TRIADE_superviseur" not in em.classes:
        raise EchecOracle(f"coquille GUI : classe absente {list(em.classes)} "
                          f"(Q1 sup-02 — V4 : jamais TRIADE_demo)")
    if "TRIADE_demo" in em.classes:
        raise EchecOracle("coquille GUI : collision lexicale avec la démo (V4 sup-02)")
    wndproc, _ = em.classes["TRIADE_superviseur"]
    if wndproc != IMAGE + 0x1640:
        raise EchecOracle(f"coquille GUI : wndproc {wndproc:#x} != scellé 0x1640 (Q1)")
    if not (em.qword(L.HWND_PRINCIPAL) and em.qword(L.HWND_JOURNAL)
            and em.qword(L.HWND_BOUTON)):
        raise EchecOracle("coquille GUI : handles absents (fenêtre/contrôles)")
    hwnd_j, hwnd_b = em.qword(L.HWND_JOURNAL), em.qword(L.HWND_BOUTON)
    if em.movewindow != [(hwnd_j, 8, 8, 764, 504), (hwnd_b, 8, 516, 764, 36)]:
        raise EchecOracle(f"coquille GUI : géométrie {em.movewindow} (V3 D36)")
    if em.journal_fichier != [TRACE_L00, TRACE_L02, TRACE_L4C, TRACE_L4D, TRACE_L01]:
        raise EchecOracle(f"coquille GUI : fichier {em.journal_fichier!r} != "
                          f"[L00, L02, L4C, L4D, L01] (V2 sup-02)")
    if em.journal != ECRAN_DEMARRAGE:
        raise EchecOracle(f"coquille GUI : ÉCRAN {em.journal!r} != {ECRAN_DEMARRAGE!r}")
    if em.messageboxes:
        raise EchecOracle("coquille GUI : MessageBoxW inattendue")
    # clic unique : spawn sup-09 une fois, L03, bouton désactivé, second ignoré
    hwnd_p = em.qword(L.HWND_PRINCIPAL)
    em.appeler(0x1640, (hwnd_p, 0x111, 1, 0))
    if em.qword(L.DRAPEAU_WORKER) != 1 or em.threads != [(IMAGE + RVA_SUP["sup-09"], 0)]:
        raise EchecOracle(f"clic : drapeau/threads {em.threads} — spawn sup-09 attendu")
    if (hwnd_b, 0) not in em.enablewindows:
        raise EchecOracle("clic : bouton non désactivé (EnableWindow FALSE)")
    em.appeler(0x1640, (hwnd_p, 0x111, 1, 0))
    if len(em.threads) != 1:
        raise EchecOracle("clic : second WM_COMMAND a relancé le scénario")
    if em.journal_fichier[-1] != TRACE_L03:
        raise EchecOracle(f"clic : trace L03 absente ({em.journal_fichier[-1]!r})")
    if em.journal[-1] != CH["L03"][1].decode("ascii") + "\r\n":
        raise EchecOracle("clic : L03 absente du miroir écran")
    return 6


def test_scenario_nominal(exe: bytes, demo17: list[bytes]):
    """Famille 5 : sup-09 complet, les DEUX variantes (D49) — publique (T3 non
    applicable, 4 lancements) et livraison (annexe intégrée, 7 lancements) :
    journal d'or, ordre, requêtes, kit posé puis retiré, nettoyage."""
    total = 0

    # --- variante PUBLIQUE : le kit vit, T3 sauté non compté, TOUT OK ---
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 1:
        raise EchecOracle(f"sup-09 nominal public : rax {r} != 1 (Q8 D49 — T3 non "
                          f"applicable n'est pas un échec)")
    _comparer_journal(em, lignes_journal_or(demo17, livraison=False),
                      "sup-09 nominal public")
    cmdlines = [p["cmdline"] for p in em.processus]
    if cmdlines != ["demo.exe", "proxy.exe", _cmd("CMD_CURL_HTTP"),
                    _cmd("CMD_CURL_HTTPS")]:
        raise EchecOracle(f"sup-09 public : lancements {[c[:20] for c in cmdlines]} "
                          f"!= 4 attendus (T3 sauté, I6)")
    # kit : les artefacts posés SONT les octets embarqués (V2), puis retirés
    blob_demo = exe[L.BLOB_FILE + 0x10: L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO]
    blob_proxy = exe[L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO:
                     L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO + L.LONGUEUR_PROXY]
    if em.fichiers_ecrits.get("C:\\sup\\demo.exe") != blob_demo:
        raise EchecOracle("sup-37 : demo.exe posé != octets embarqués (V2 — "
                          "le disque doit porter l'artefact scellé)")
    if em.fichiers_ecrits.get("C:\\sup\\proxy.exe") != blob_proxy:
        raise EchecOracle("sup-37 : proxy.exe posé != octets embarqués (V2)")
    if "C:\\sup\\terrain_jetons.bin" in em.fichiers_ecrits:
        raise EchecOracle("sup-37 : annexe posée en variante publique (V3 — "
                          "le slot vide ne doit jamais écrire l'annexe)")
    supprimees = [s.rsplit("\\", 1)[-1] for s in em.suppressions]
    for nom in ("demo.exe", "proxy.exe", "terrain_jetons.bin",
                "terrain_page_http.txt", "terrain_page_https.txt"):
        if nom not in supprimees:
            raise EchecOracle(f"nettoyage kit : {nom} non supprimé (Q6 sup-37 — "
                              f"le dossier ne garde que le journal)")
    if "C:\\sup\\demo.exe" in em.fichiers or "C:\\sup\\proxy.exe" in em.fichiers:
        raise EchecOracle("nettoyage kit : un artefact survit au run (Q6)")
    total += 7

    # --- variante LIVRAISON (jetons FICTIFS au slot) : le run intégral ---
    exe_l = variante_livraison(exe)
    em = Emulateur(exe_l)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 1:
        raise EchecOracle(f"sup-09 nominal livraison : rax {r} != 1 (Q6 — TOUT OK attendu)")
    _comparer_journal(em, lignes_journal_or(demo17, livraison=True),
                      "sup-09 nominal livraison")
    if em.fichiers_ecrits.get("C:\\sup\\terrain_jetons.bin") != JETONS:
        raise EchecOracle("sup-37 : annexe posée != annexe du slot (V2 — la "
                          "variante livraison porte ses jetons)")

    # I2/I4 sup-09 : ordre ET composition exacte des 7 lancements
    cmdlines = [p["cmdline"] for p in em.processus]
    attendus = ["demo.exe", "proxy.exe", _cmd("CMD_CURL_HTTP"),
                _cmd("CMD_CURL_HTTPS"), CMD_JETON_ATTENDU,
                CMD_SESSION_ATTENDU, CMD_PUT_ATTENDU]
    if cmdlines != attendus:
        for i, (obtenu, attendu) in enumerate(zip(cmdlines, attendus)):
            if obtenu != attendu:
                raise EchecOracle(f"sup-09 : lancement #{i + 1} divergent :\n"
                                  f"  obtenu  {obtenu!r}\n  attendu {attendu!r} "
                              f"(I2 ordre T1->T2->T3 + composition)")
        raise EchecOracle(f"sup-09 : {len(cmdlines)} lancements != 7 : "
                          f"{[c[:30] for c in cmdlines]}")

    # sup-31 V2 : héritage et cwd par lancement (D36 : cwd forcé)
    par_cmd = {p["cmdline"]: p for p in em.processus}
    demo_p = next(p for p in em.processus if p["cmdline"].startswith("demo.exe"))
    if demo_p["herite"] != 0 or demo_p["si_flags"] & 0x100:
        raise EchecOracle("sup-31 : demo.exe lancé avec héritage/tuyaux (I4/Q6)")
    proxy_p = next(p for p in em.processus if p["cmdline"].startswith("proxy.exe"))
    if proxy_p["herite"] != 1 or not proxy_p["si_flags"] & 0x100:
        raise EchecOracle("sup-31 : proxy.exe sans tuyaux/héritage (Q1/Q2 mode 1)")
    for p in em.processus:
        # le répertoire forcé conserve le séparateur (troncature au '\', NUL
        # posé APRÈS — D36) : "C:\sup\" est un chemin valide pour CreateProcess
        if p["cwd"] not in ("C:\\sup", "C:\\sup\\") or not p["cwd"]:
            raise EchecOracle(f"sup-31 : cwd {p['cwd']!r} != répertoire de l'exe "
                              f"(Q3 — le correctif D36 a disparu)")
    for p in em.processus:
        if p["cmdline"].startswith("curl.exe") and (p["herite"] != 0 or p["si_flags"] & 0x100):
            raise EchecOracle("sup-34 : curl lancé AVEC tuyaux — .curl devait "
                              "poser edx = 0 (défaut mode corrigé)")

    # sup-34 : quit écrit sur stdin AVANT l'attente du proxy (V5)
    if em.stdin_proxy != b"quit\r\n":
        raise EchecOracle(f"sup-34 : stdin du proxy {em.stdin_proxy!r} != quit (Q6)")
    h_proxy = next(p["hproc"] for p in em.processus
                   if p["cmdline"].startswith("proxy.exe"))
    seq_stdin = [i for i, (_n, e, _d) in enumerate(em.sequence) if e == "stdin"]
    seq_attente_proxy = [i for i, (_n, e, d) in enumerate(em.sequence)
                         if e == "attente" and d == hex(h_proxy)]
    if not seq_stdin or not seq_attente_proxy or seq_stdin[0] > seq_attente_proxy[0]:
        raise EchecOracle("sup-34 : quit non écrit avant l'attente du proxy (V5)")

    # sup-35 : requêtes composées octet par octet (V2 — le miroir d'écriture
    # survit au nettoyage qui supprime les 5 temporaires)
    if em.fichiers_ecrits.get("C:\\sup\\terrain_req.txt") != REQ_OAUTH_ATTENDUE:
        raise EchecOracle(f"sup-35 : requête OAuth {em.fichiers_ecrits.get('C:\\sup\\terrain_req.txt')!r} "
                          f"!= composition attendue (Q2)")
    if em.fichiers_ecrits.get("C:\\sup\\terrain_meta.json") != META_ATTENDUE:
        raise EchecOracle(f"sup-35 : métadonnées {em.fichiers_ecrits.get('C:\\sup\\terrain_meta.json')!r} "
                          f"!= {{name:TAMPON_NOM, parents:[dossier]}} (Q5)")
    put = next((p for p in em.processus if p["cmdline"].startswith("curl.exe")
                and "PUT" in p["cmdline"]), None)
    if put is None or put["cmdline"] != CMD_PUT_ATTENDU:
        raise EchecOracle(f"sup-35 : PUT {put and put['cmdline']!r} != "
                          f"--data-binary @<BUF_CHEMIN> <URL session> (Q7/I2)")

    # nettoyage : 2 pages (T2) + 5 temporaires (T3) + 3 kit (sup-37) — zéro fuite
    supprimees = [s.rsplit("\\", 1)[-1] for s in em.suppressions]
    for nom in ("terrain_page_http.txt", "terrain_page_https.txt",
                "terrain_req.txt", "terrain_jeton.json", "terrain_meta.json",
                "terrain_session.txt", "terrain_rep.json",
                "demo.exe", "proxy.exe", "terrain_jetons.bin"):
        if nom not in supprimees:
            raise EchecOracle(f"nettoyage : {nom} non supprimé "
                              f"(Q8 sup-34/Q9 sup-35/Q6 sup-37 — zéro résidu)")
    if PIPE_IN_WR not in em.handles_fermes or PIPE_OUT_RD not in em.handles_fermes:
        raise EchecOracle("sup-34 : extrémités parent des tuyaux non fermées (Q8)")

    # I1 sup-35 : AUCUN secret au journal
    journal_brut = b"".join(em.journal_fichier)
    for secret in (b"client-id-test", b"GOCSPX-test-secret", b"//test-refresh-token",
                   JETON_OAUTH):
        if secret in journal_brut:
            raise EchecOracle(f"sup-35 : secret {secret[:12]!r}… présent au journal "
                              f"(I1 — le constat ne fuit pas ses clés)")
    total += 12
    return total


def test_echecs(exe: bytes, demo17: list[bytes]):
    """Famille 6 : échec GUI + 5 scénarios dégradés — un KO n'arrête rien."""
    total = 0
    # (a) RegisterClassExW = 0 -> MessageBoxW + LKO gle + sortie 1 (E1 sup-02)
    em = Emulateur(exe)
    em.installer_shims()
    em.horloge = HORLOGE_NOMINALE
    em.retour_register = 0
    em.gle = 87
    em.appeler(RVA_SUP["sup-01"])
    if em.code_sortie != 1 or len(em.messageboxes) != 1:
        raise EchecOracle("échec GUI : sortie/MessageBoxW attendues (E1 sup-02)")
    attendu_ko = [TRACE_L00, CH["LKO_GUI"][1] + b"87\r\n"]
    if em.journal_fichier != attendu_ko:
        raise EchecOracle(f"échec GUI : fichier {em.journal_fichier!r} != {attendu_ko!r}")
    total += 2

    # (b) demo.exe absent -> S10B, T2/T3 vivent quand même (E1 sup-33, E2 sup-09)
    em = Emulateur(variante_livraison(exe))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.fichiers.pop("C:\\sup\\demo_journal.txt")
    em.echec_createprocess = ["demo.exe"]
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("démo absente : verdict final != 0 (E2 sup-09)")
    brut = b"".join(em.journal_fichier)
    if S("S10B") + b"\r\n" not in brut:
        raise EchecOracle("démo absente : S10B absent du journal (E1 sup-33)")
    if S("S28A") + b"\r\n" not in brut or S("S36A") + b"\r\n" not in brut:
        raise EchecOracle("démo absente : T2/T3 n'ont pas vécu leurs verdicts "
                          "(l'indépendance des tests est le cœur du superviseur)")
    if S("S11A") + b"\r\n" in brut:
        raise EchecOracle("démo absente : S11A émis sans fenêtre (E1)")
    total += 3

    # (c) journal démo non conforme : 16 lignes, marqueur absent (E3 sup-33)
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    demo16 = demo17[:-1]                      # J_FINAL retiré
    preparer_scenario(em, demo16)
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("journal non conforme : verdict final != 0")
    brut = b"".join(em.journal_fichier)
    if S("S14") + b"16" + b"\r\n" not in brut:
        raise EchecOracle("journal non conforme : S14 lignes=16 absent (E3)")
    if S("S15B") + b"\r\n" not in brut or S("S16B") + b"\r\n" not in brut:
        raise EchecOracle("journal non conforme : verdict NON conforme absent (E3)")
    if latin1("TRIADE M2 — démonstration") not in brut:
        raise EchecOracle("journal non conforme : le journal PARTIEL devait quand "
                          "même être embarqué (localise l'intervalle — leçon demo.3)")
    total += 3

    # (d) curl http code 22 -> S22 code=22, verdict T2 KO, le reste exécuté (E3)
    em = Emulateur(variante_livraison(exe))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17, code_curl_http=22)
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("curl KO : verdict final != 0")
    brut = b"".join(em.journal_fichier)
    if S("S22A") + b"22" + b"\r\n" not in brut:
        raise EchecOracle("curl KO : S22 code=22 absent (E3 sup-34)")
    if S("S28B") + b"\r\n" not in brut:
        raise EchecOracle("curl KO : verdict T2 KO absent (pas de court-circuit)")
    if S("S36A") + b"\r\n" not in brut:
        raise EchecOracle("curl KO : T3 n'a pas vécu son verdict")
    total += 3

    # (e) annexe déclarée mais non posable (livraison, écriture refusée) ->
    #     S06C, T3 tourne quand même (bit 2 = 1 : échec honnête), S31/S36B,
    #     aucun curl Drive (E1/E3 sup-35 + E3 sup-37)
    em = Emulateur(variante_livraison(exe))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.echec_createfile_chemins = {"C:\\sup\\terrain_jetons.bin"}
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("annexe non posable : verdict final != 0 (E3 — T3 compte)")
    brut = b"".join(em.journal_fichier)
    if S("S06C") + b"\r\n" not in brut:
        raise EchecOracle("annexe non posable : S06C absent (E3 sup-37)")
    if S("S31") + b"\r\n" not in brut or S("S36B") + b"\r\n" not in brut:
        raise EchecOracle("annexe non posable : S31/S36B absents (E1 sup-35)")
    spawns = [d for (_, e, d) in em.sequence if e == "spawn"]
    if any("oauth" in s or "googleapis" in s or "PUT" in s for s in spawns):
        raise EchecOracle("annexe non posable : un curl Drive a été lancé (E1)")
    total += 3

    # (f) réponse OAuth muette -> S33B, session non tentée (E2 sup-35)
    em = Emulateur(variante_livraison(exe))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17, reponse_oauth=b'{"error":"invalid_grant"}')
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("OAuth muet : verdict final != 0")
    brut = b"".join(em.journal_fichier)
    if S("S33B") + b"\r\n" not in brut or S("S36B") + b"\r\n" not in brut:
        raise EchecOracle("OAuth muet : S33B/S36B absents (E2 sup-35)")
    spawns = [d for (_, e, d) in em.sequence if e == "spawn"]
    if any("Authorization" in s or "PUT" in s for s in spawns):
        raise EchecOracle("OAuth muet : session/PUT tentés sans jeton (I5)")
    total += 3

    # (g) extraction demo.exe impossible (public) -> S04D, T1 sauté COMPTÉ
    #     ÉCHEC, T2 vit, nettoyage quand même (E1 sup-37 + E3 sup-09)
    em = Emulateur(exe)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.echec_createfile_chemins = {"C:\\sup\\demo.exe"}
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("extraction impossible : TOUT OK usurpé (E3 — un test "
                          "non prouvé ne vaut jamais vert)")
    brut = b"".join(em.journal_fichier)
    if S("S04D") + b"\r\n" not in brut:
        raise EchecOracle("extraction impossible : S04D absent (E1 sup-37)")
    if S("S10") + b"\r\n" in brut:
        raise EchecOracle("extraction impossible : T1 a été lancé sans artefact")
    if S("S28A") + b"\r\n" not in brut or S("S07A") + b"\r\n" not in brut:
        raise EchecOracle("extraction impossible : T2/nettoyage devaient vivre")
    total += 3

    # (h) écart à la relecture (livraison, octet retourné modifié) -> S05B,
    #     T2 sauté compté échec, T1/T3 vivent (E2 sup-37)
    em = Emulateur(variante_livraison(exe))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.corrompre_lecture = ("C:\\sup\\proxy.exe", 100)
    r = em.appeler(RVA_SUP["sup-09"])
    if r != 0:
        raise EchecOracle("écart relecture : TOUT OK usurpé (E2 sup-37)")
    brut = b"".join(em.journal_fichier)
    if S("S05B") + b"\r\n" not in brut:
        raise EchecOracle("écart relecture : S05B absent (E2 sup-37)")
    if S("S20") + b"\r\n" in brut:
        raise EchecOracle("écart relecture : T2 a été lancé sur un artefact écarté")
    if S("S16A") + b"\r\n" not in brut or S("S36A") + b"\r\n" not in brut:
        raise EchecOracle("écart relecture : T1/T3 devaient vivre leur verdict")
    total += 3
    return total


def test_falsification(exe: bytes, demo17: list[bytes]):
    """Famille 7 : porte R10 sur tout + 5 mutations ciblées attrapées."""
    total = 0
    detectees = 0
    cibles = _blocs_terrain() + [("zone-sup-1", L.ZONE_DATA_SUP[0]),
                                 ("zone-sup-2", L.ZONE_DATA_SUP_2[0]),
                                 ("zone-sup-3", L.ZONE_DATA_SUP_3[0]),
                                 ("zone-blob", L.BLOB_RVA)]
    for bid, rva in cibles:
        for offset in (11, 23):
            mutant = bytearray(exe)
            mutant[_fichier_rva(rva) + offset] ^= 0xFF
            try:
                em2 = Emulateur(bytes(mutant))
                em2.installer_shims()
                r2 = em2.appeler(RVA_SUP["win-06"])
            except Exception:
                detectees += 1     # crash = détection (fail-closed, leçon D47)
                break
            if r2 == 4:
                if offset == 23:
                    raise EchecOracle(f"falsification : {bid} (octet {offset}) "
                                      f"non détecté — la porte est aveugle")
                continue
            detectees += 1
            break
        else:
            raise EchecOracle(f"falsification : {bid} non détecté par la porte R10")
    total += detectees

    def muter(motif: bytes, remplacement: bytes, zone: tuple, nom: str) -> bytes:
        base = _fichier_rva(zone[0])
        tranche = exe[base:base + (zone[1] - zone[0])]
        pos = tranche.find(motif)
        if pos < 0:
            raise EchecOracle(f"falsification {nom} : motif {motif.hex()} introuvable")
        mutant = bytearray(exe)
        mutant[base + pos:base + pos + len(motif)] = remplacement
        return bytes(mutant)

    # M1 : constante 17 -> 18 dans sup-33 (V5) — 17 lignes servies, 18 exigées
    mutant = muter(bytes.fromhex("4183fd11"), bytes.fromhex("4183fd12"),
                   L.ZONE_T1, "constante 17")
    em = Emulateur(mutant)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    if em.appeler(RVA_SUP["sup-33"]) == 1:
        raise EchecOracle("falsification constante 17 : T1 VERTE avec 18 lignes "
                          "exigées — le verdict n'est pas une preuve (V5 sup-33)")
    total += 1

    # M2 : longueur d'étiquette 16 -> 15 dans sup-35 (V5) — extraction cassée
    mutant = muter(bytes.fromhex("41b910000000"), bytes.fromhex("41b90f000000"),
                   L.ZONE_T3, "étiquette 16")
    em = Emulateur(mutant)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    if em.appeler(RVA_SUP["sup-35"]) == 1:
        raise EchecOracle("falsification étiquette : T3 VERTE avec une étiquette "
                          "raccourcie — un jeton raccourci ne doit jamais circuler "
                          "(E2 sup-22)")
    total += 1

    # M3 : ordre T1/T2 inversé dans sup-09 (V5) — le journal téléversé serait
    # incomplet ; le verrou d'ordre de l'oracle doit s'y opposer
    base = _fichier_rva(L.ZONE_SCENARIO[0])
    tranche = exe[base:base + 0x200]
    appels = []
    for i in range(len(tranche) - 4):
        if tranche[i] == 0xE8:
            disp = struct.unpack_from("<i", tranche, i + 1)[0]
            cible = L.ZONE_SCENARIO[0] + i + 5 + disp
            appels.append((i, cible))
    t1 = next(a for a in appels if a[1] == RVA_SUP["sup-33"])
    t2 = next(a for a in appels if a[1] == RVA_SUP["sup-34"])
    mutant = bytearray(exe)
    struct.pack_into("<i", mutant, base + t1[0] + 1,
                     RVA_SUP["sup-34"] - (L.ZONE_SCENARIO[0] + t1[0] + 5))
    struct.pack_into("<i", mutant, base + t2[0] + 1,
                     RVA_SUP["sup-33"] - (L.ZONE_SCENARIO[0] + t2[0] + 5))
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    r = em.appeler(RVA_SUP["sup-09"])
    try:
        _comparer_journal(em, lignes_journal_or(demo17), "ordre T1/T2/T3")
        raise EchecOracle("falsification ordre : le journal d'or a accepté T2 "
                          "avant T1 — le verrou d'ordre ne garde rien (I2 sup-09)")
    except EchecOracle as exc:
        if "ordre T1/T2/T3" not in str(exc):
            raise
    total += 1

    # M4 : nettoyage 5 -> 4 dans sup-35 (V5) — un temporaire survit
    mutant = muter(bytes.fromhex("41bd05000000"), bytes.fromhex("41bd04000000"),
                   L.ZONE_T3, "nettoyage 5")
    em = Emulateur(mutant)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.appeler(RVA_SUP["sup-35"])
    supprimees = [s.rsplit("\\", 1)[-1] for s in em.suppressions]
    if len([s for s in supprimees if s.startswith("terrain_")]) >= 5:
        raise EchecOracle("falsification nettoyage : 5 suppressions malgré la "
                          "constante corrompue — le verrou zéro résidu est muet")
    total += 1

    # M5 : quit raccourci (6 -> 0) dans sup-34 (V5) — rien sur stdin
    mutant = muter(bytes.fromhex("41b806000000"), bytes.fromhex("41b800000000"),
                   L.ZONE_T2, "quit 6")
    em = Emulateur(mutant)
    em.installer_shims()
    em.uc.mem_write(IMAGE + L.HWND_JOURNAL, struct.pack("<Q", FAKE_HWND_EDIT))
    preparer_scenario(em, demo17)
    em.appeler(RVA_SUP["sup-34"])
    if em.stdin_proxy:
        raise EchecOracle("falsification quit : stdin non vide malgré la longueur "
                          "corrompue — « quit écrit avant arret » est muet")
    total += 1
    return total, detectees, len(cibles)


# =============================================================================
# Point d'entrée
# =============================================================================

def executer(exe: bytes, graine: int = 1) -> dict:
    global JOURNAL_DEMO_17
    total, verdicts = 0, {}
    JOURNAL_DEMO_17 = _journal_demo_17()

    # 0. win-06 : porte R10 + vecteurs libc (l'image doit être saine)
    em = Emulateur(exe)
    em.installer_shims()
    r = em.appeler(RVA_SUP["win-06"])
    if r != 4:
        raise EchecOracle(f"win-06 : eax = {r} != 4 (porte + 4 vecteurs attendus)")
    verdicts["d40006"] = {"cas": 5, "detail": "porte R10 verte (table 27 entrées + terminateur, "
                                               "4 zones + blob, D49) + 4/4 libc"}
    total += 5
    mutant = bytearray(exe)
    struct.pack_into("<Q", mutant, L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA), 0x00020000)
    em = Emulateur(bytes(mutant))
    em.installer_shims()
    if em.appeler(RVA_SUP["win-06"]) != 0xFFFFFFFF:
        raise EchecOracle("win-06 : version sous plancher non détectée")
    total += 1

    n = test_differentiel_balaye(exe, graine)
    verdicts["f60022"] = {"cas": n, "detail": "différentiel 10 000 cas contraints "
                                               "vs référence Python (pur, I3)"}
    total += n

    n = test_horodatage(exe)
    verdicts["f60021"] = {"cas": n, "detail": "3 horloges fixes — nom du run et "
                                               "ligne S01 octet par octet, rax 24"}
    total += n

    n = test_journal_sup11(exe)
    verdicts["f60011"] = {"cas": n, "detail": "modes 0/1/2, chemin horodaté, paresse, "
                                               "échec/re-tentative, multi-lignes, V7 différenciation"}
    total += n

    n = test_coquille_gui(exe)
    verdicts["f60001"] = {"cas": 3, "detail": "entrée -> horodatage AVANT fenêtre "
                                               "(ordre prouvé) -> boucle -> sortie 0"}
    verdicts["f60002"] = {"cas": 3, "detail": "classe TRIADE_superviseur validée, "
                                               "wndproc scellé, L00/L01, géométrie 764/504"}
    total += n

    n = test_scenario_nominal(exe, JOURNAL_DEMO_17)
    verdicts["f60009"] = {"cas": n, "detail": "scénario COMPLET x2 variantes (publique "
                                               "4 lancements + livraison 7) : journal d'or, cwd forcé, "
                                               "quit<attente, requêtes exactes, kit posé/relu/retiré"}
    verdicts["f60031"] = {"cas": 3, "detail": "mode 0 muet / mode 1 tuyaux+héritage, "
                                               "cwd répertoire exe (D36), zéro fuite"}
    verdicts["f60033"] = {"cas": 3, "detail": "T1 vert : fenêtre au 3e sondage, clic "
                                               "BM_CLICK, marqueur 31 o, 17 lignes embarquées"}
    verdicts["f60034"] = {"cas": 3, "detail": "T2 vert : bannière/événements/arret "
                                               "memcmp exacts, curl sans tuyaux, flux embarqué"}
    verdicts["f60035"] = {"cas": 3, "detail": "T3 vert : OAuth/métadonnées/session/PUT "
                                               "composés exacts, 5 suppressions, zéro secret"}
    verdicts["f60037"] = {"cas": 6, "detail": "kit embarqué : demo/proxy posés puis "
                                               "relus octet conformes, annexe selon variante, "
                                               "échec écriture + écart relecture, nettoyage"}
    total += n + 6

    n = test_echecs(exe, JOURNAL_DEMO_17)
    verdicts["echecs"] = {"cas": n, "detail": "GUI KO + démo absente + journal non "
                                               "conforme + curl 22 + annexe non posable + OAuth muet + "
                                               "extraction impossible + écart relecture — jamais de court-circuit"}
    total += n

    n, detectees, nb_cibles = test_falsification(exe, JOURNAL_DEMO_17)
    falsification = f"{detectees}/{nb_cibles} cibles R10 détectées (octets 11/23) + " \
                    f"5 mutations ciblées attrapées"
    verdicts["falsification"] = {"cas": n, "detail": falsification}
    total += n

    empreinte = hashlib.sha256(
        json.dumps({k: v for k, v in verdicts.items()}, sort_keys=True).encode("ascii")
        + f"|graine={graine}".encode("ascii")).hexdigest()
    return {"total_cas": total, "blocs": verdicts, "falsification": falsification,
            "empreinte": "sha256:" + empreinte, "graine": graine}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("exe", nargs="?", default=os.path.join(ICI, "superviseur.exe"))
    ap.add_argument("--graine", type=int, default=1)
    args = ap.parse_args()
    with open(args.exe, "rb") as f:
        donnees = f.read()
    verdict = executer(donnees, graine=args.graine)
    print(f"[oracle terrain] {verdict['total_cas']} cas verts ; "
          f"falsification : {verdict['falsification']}")
    print(f"[empreinte] {verdict['empreinte']}")

