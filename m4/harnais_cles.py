#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_cles.py — Harnais à propriétés de tls-05 (cycle de vie des handles, D81).

Premier bloc À SHIMS du jalon M4 : la notation appelle l'IAT secur32
(AcquireCredentialsHandleW / DeleteSecurityContext / FreeCredentialsHandle)
et route chaque HRESULT par la VRAIE tls-02 (octets de sa notation, intégration
testée). Vecteurs de la spécification tls-05:R1 :

  V1  round-trip de notation 100 % (taille totale == « Code : N o ») ;
  V2  oracle à shims (scénarios de la spec) : acquisition/déstruction/
      libération en succès ; acquisition en échec ; libération en échec ;
      opérations hors domaine — états du cadre OCTET PAR OCTET prédits
      avant/après chaque appel, contrat D'APPELS complet (9 arguments de
      l'acquisition vérifiés : principal NULL, package fixture EXACT,
      OUTBOUND, pAuthData NULL — P3, la validation AUTOMATIQUE n'est jamais
      désactivée —, phCredential = cadre+0) ;
  V3  fuzzing à propriétés : opérations valides ET hostiles, HRESULT
      documentés ET exotiques, handles magiques aléatoires écrits par les
      shims — le verdict suit tls-02 (modèle écrit depuis la SPÉCIFICATION
      via layout.HRESULTS), le cadre ne change QUE sur succès constaté,
      canaris mémoire, non-volatils sentinelles ;
  V4  falsification : SIX mutations D'UN SEUL point de la notation doivent
      être ATTRAPÉES par le différentiel ; le témoin intact reste vert.

Le harnais émule les octets de la NOTATION (ce que build_m4.py embarquera) à
ses RVA .text3 exacts, l'IAT secur32 ARRÊTÉE D81 (slots .rdata 0x2A00… reçoivent
les fausses adresses — résolution chargeur, mécanisme M2/M3), la fixture
package à 0x2C00 et tls-02 à 0x6080.
Usage : python3 harnais_cles.py [--graine G] [--cas N]
"""

from __future__ import annotations

import argparse
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
import layout as L  # noqa: E402

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15, UC_X86_REG_RIP)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15, "rip": UC_X86_REG_RIP}

# --- Mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ----------

ZONE_CODE = 0x6000            # page .text3 : tls-02 @ 0x6080, tls-05 @ 0x65C0
TAILLE_CODE = 0x1000
RET_MAGIQUE = 0x6F00          # adresse d'arrêt propre (int3 de la page code)
ZONE_RDATA = 0x2000           # page .rdata M4 : IAT secur32 + fixture package
TAILLE_RDATA = 0x1000
TRAMPOLINE = 0x140100000      # fausses adresses d'API (page RX, mécanisme M2/M3)
ZONE_CADRE = 0x150000000      # cadre de session TLS (+ canaris)
TAILLE_CADRE_PAGE = 0x1000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

RVA_TLS02, SLOT_TLS02 = 0x6080, 0x100
RVA_TLS05, SLOT_TLS05 = 0x65C0, 0x180

FAUX = {nom: TRAMPOLINE + (i + 1) * 0x10
        for i, nom in enumerate(L.SECUR32_IMPORTS)}
FAUX_REV = {v: k for k, v in FAUX.items()}

CANARI = b"\xA5"
SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x89898989898989,
}
CHAMPS_SENTINELLES = {"socket": 0x5555555555555555, "ptr_nom": 0x6666666666666666}

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


# --- V1 : round-trip ------------------------------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f:
            ligne = brut.split(";")[0].strip()
            if ligne:
                lignes.append(ligne)
    return lignes


def assembler_lignes(ks: Ks, lignes: list[str], rva: int) -> bytes:
    sortie, adresse = [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise RuntimeError(f"ligne inassemblable à 0x{adresse:x} : {ligne!r}")
        sortie.append(bytes(enc))
        adresse += len(enc)
    return b"".join(sortie)


def octets_notation(ks: Ks, bloc: str, rva: int, mutation: tuple[str, str] | None = None):
    chemin = os.path.join(ICI, "notation", bloc + ".asm")
    lignes = lignes_notation(chemin)
    declare = None
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("; Code : "):
                declare = int(ligne.split("Code : ")[1].split(" o ")[0])
    if mutation:
        avant, apres = mutation
        cibles = [i for i, l in enumerate(lignes) if avant in l]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation ambiguë ({len(cibles)} occurrences) : {avant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(avant, apres)
        return assembler_lignes(ks, lignes, rva), None
    return assembler_lignes(ks, lignes, rva), declare


# --- Modèle de référence (écrit depuis la SPÉCIFICATION — jamais la notation) -----

def verdict_modele(hresult: int) -> int:
    """tls-02:R1 via la liste blanche de la spécification (layout.HRESULTS)."""
    return L.HRESULTS.get(hresult & 0xFFFFFFFF, L.VERDICT_FATAL)


def modele_tls05(op: int, cadre0: dict, hresult: int, magic: tuple[int, int]):
    """Retourne (verdict, cadre_attendu, appels_attendus).

    Q1 : op 0 — succès : handle écrit PAR la bibliothèque (magic) ; échec :
         cadre intact PAR CONSTRUCTION (remise à zéro défensive — rien d'acquis
         ne reste à compenser). Q2/Q3 : op 1/2 — remise à zéro APRÈS un succès
         constaté, jamAIS avant l'appel ; échec : inchangé, verdict retourné
         tel quel (Q4). Hors domaine (P1 violé) : refus défensif verdict 6,
         aucun appel, cadre intact.
    """
    cadre = dict(cadre0)
    if op == 0:
        v = verdict_modele(hresult)
        appels = [("ACH", None)]
        if v == 0:
            cadre["cred_lo"], cadre["cred_hi"] = magic
        else:
            cadre["cred_lo"], cadre["cred_hi"] = 0, 0
        return v, cadre, appels
    if op == 1:
        v = verdict_modele(hresult)
        appels = [("DSC", L.CADRE_CTXT)]
        if v == 0:
            cadre["ctxt_lo"], cadre["ctxt_hi"] = 0, 0
        return v, cadre, appels
    if op == 2:
        v = verdict_modele(hresult)
        appels = [("FCH", L.CADRE_CRED)]
        if v == 0:
            cadre["cred_lo"], cadre["cred_hi"] = 0, 0
        return v, cadre, appels
    return 6, cadre, []


def cadre_initial(cred=(0, 0), ctxt=(0x3333333333333333, 0x4444444444444444)) -> dict:
    return {"cred_lo": cred[0], "cred_hi": cred[1],
            "ctxt_lo": ctxt[0], "ctxt_hi": ctxt[1],
            "socket": CHAMPS_SENTINELLES["socket"],
            "ptr_nom": CHAMPS_SENTINELLES["ptr_nom"]}


def ecrire_cadre(uc: Uc, cadre: dict):
    zone = bytearray(CANARI * TAILLE_CADRE_PAGE)
    def q(offset, valeur):
        zone[offset:offset + 8] = struct.pack("<Q", valeur & 0xFFFFFFFFFFFFFFFF)
    q(L.CADRE_CRED, cadre["cred_lo"]); q(L.CADRE_CRED + 8, cadre["cred_hi"])
    q(L.CADRE_CTXT, cadre["ctxt_lo"]); q(L.CADRE_CTXT + 8, cadre["ctxt_hi"])
    q(L.CADRE_SOCKET, cadre["socket"]); q(L.CADRE_PTR_NOM, cadre["ptr_nom"])
    uc.mem_write(ZONE_CADRE, bytes(zone))


def lire_cadre(uc: Uc) -> dict:
    def q(offset):
        return struct.unpack("<Q", bytes(uc.mem_read(ZONE_CADRE + offset, 8)))[0]
    return {"cred_lo": q(L.CADRE_CRED), "cred_hi": q(L.CADRE_CRED + 8),
            "ctxt_lo": q(L.CADRE_CTXT), "ctxt_hi": q(L.CADRE_CTXT + 8),
            "socket": q(L.CADRE_SOCKET), "ptr_nom": q(L.CADRE_PTR_NOM)}


# --- Émulateur à shims SSPI (mécanisme M2/M3 : page ret + crochet code) -----------

class Emulateur:
    """Un chargement = un émulateur NEUF (leçon D79 : le cache de traduction
    unicorn n'est pas invalidé par mem_write sur du code exécuté). Les shims
    SSPI sont scriptés par cas : (HRESULT à retourner, handles magiques)."""

    def __init__(self, blob_tls05: bytes, blob_tls02: bytes):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_CODE, TAILLE_CODE)
        uc.mem_map(ZONE_RDATA, TAILLE_RDATA)
        uc.mem_map(TRAMPOLINE, 0x1000)
        uc.mem_map(ZONE_CADRE, TAILLE_CADRE_PAGE)
        uc.mem_map(ZONE_PILE, TAILLE_PILE)
        page = b"\xCC" * TAILLE_CODE
        for rva, blob in ((RVA_TLS02, blob_tls02), (RVA_TLS05, blob_tls05)):
            page = page[:rva - ZONE_CODE] + blob + page[rva - ZONE_CODE + len(blob):]
        uc.mem_write(ZONE_CODE, page)
        uc.mem_write(TRAMPOLINE, b"\xc3" * 0x1000)       # chaque shim retourne
        # résolution chargeur : les slots IAT secur32 reçoivent les fausses adresses
        for nom, rva in L.IAT_SEC32_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        # fixture .rdata M4 : le package Schannel (tls-05, unique propriétaire)
        uc.mem_write(L.R_PKG_M4, L.PKG_M4)
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE, end=TRAMPOLINE + 0x1000)
        self.script_hresult = 0
        self.script_magic = (0, 0)
        self.appels: list[tuple] = []                     # trace (nom, détails)
        self.faux_pas = []                                # comportements impossibles

    def _shim(self, uc: Uc, adresse: int, taille: int, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            raise RuntimeError(f"shim inconnu @{adresse:#x}")
        getattr(self, "_api_" + nom)()

    def _pile(self, offset: int) -> int:
        """Argument pile de l'appelant, vu du shim ([rsp+0x28] = arg5 msx64)."""
        rsp = self.uc.reg_read(REGS["rsp"])
        return struct.unpack("<Q", bytes(self.uc.mem_read(rsp + offset, 8)))[0]

    def _api_AcquireCredentialsHandleW(self):
        uc = self.uc
        principal = uc.reg_read(REGS["rcx"])
        pkg = uc.reg_read(REGS["rdx"])
        usage = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        logonid = uc.reg_read(REGS["r9"])
        authdata = self._pile(0x28)
        getkey = self._pile(0x30)
        getkeyarg = self._pile(0x38)
        phcred = self._pile(0x40)
        expiry = self._pile(0x48)
        # la fixture package doit être EXACTE (contrat d'appel, propriétaire unique)
        pkg_lu = bytes(uc.mem_read(pkg, len(L.PKG_M4))) if pkg else b""
        self.appels.append(("ACH", principal, pkg, usage, logonid, authdata,
                            getkey, getkeyarg, phcred, expiry, pkg_lu))
        uc.reg_write(REGS["rax"], self.script_hresult & 0xFFFFFFFF)
        # sur succès la bibliothèque écrit le handle ; sur échec elle peut
        # barbouiller — le bloc doit garantir un cadre intact dans les DEUX cas
        if self.script_hresult == 0:
            uc.mem_write(phcred, struct.pack("<QQ", *self.script_magic))
        else:
            uc.mem_write(phcred, struct.pack("<QQ", 0xDEAD, 0xBEEF))

    def _api_DeleteSecurityContext(self):
        self.appels.append(("DSC", self.uc.reg_read(REGS["rcx"])))
        self.uc.reg_write(REGS["rax"], self.script_hresult & 0xFFFFFFFF)

    def _api_FreeCredentialsHandle(self):
        self.appels.append(("FCH", self.uc.reg_read(REGS["rcx"])))
        self.uc.reg_write(REGS["rax"], self.script_hresult & 0xFFFFFFFF)

    def _api_InitializeSecurityContextW(self):
        self.faux_pas.append("ISC appelé par tls-05 (I1 violée)")

    def _api_QueryContextAttributesW(self):
        self.faux_pas.append("QCA appelé par tls-05 (I1 violée)")

    def _api_EncryptMessage(self):
        self.faux_pas.append("EM appelé par tls-05 (I1 violée)")

    def _api_DecryptMessage(self):
        self.faux_pas.append("DM appelé par tls-05 (I1 violée)")

    def executer(self, op: int, hresult: int, magic: tuple[int, int]) -> tuple[int, dict]:
        uc = self.uc
        self.script_hresult = hresult & 0xFFFFFFFF
        self.script_magic = magic
        self.appels = []
        self.faux_pas = []
        ecrire_cadre(uc, cadre_initial())
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP)
        uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], op & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(REGS["rdx"], ZONE_CADRE)
        uc.reg_write(REGS["r8"], 0xAAAAAAAA)
        uc.reg_write(REGS["r9"], 0xBBBBBBBB)
        uc.emu_start(RVA_TLS05, RET_MAGIQUE, timeout=2_000_000, count=100_000)
        return self.uc.reg_read(REGS["rax"]) & 0xFFFFFFFF, lire_cadre(uc)

    def hygiene(self, cadre_attendu: dict) -> list[str]:
        """Écarts d'hygiène : canaris, non-volatils, IAT, fixture, faux pas."""
        problemes = list(self.faux_pas)
        page = bytes(self.uc.mem_read(ZONE_CADRE, TAILLE_CADRE_PAGE))
        attendu = bytearray(CANARI * TAILLE_CADRE_PAGE)
        def q(offset, valeur):
            attendu[offset:offset + 8] = struct.pack("<Q", valeur & 0xFFFFFFFFFFFFFFFF)
        q(L.CADRE_CRED, cadre_attendu["cred_lo"]); q(L.CADRE_CRED + 8, cadre_attendu["cred_hi"])
        q(L.CADRE_CTXT, cadre_attendu["ctxt_lo"]); q(L.CADRE_CTXT + 8, cadre_attendu["ctxt_hi"])
        q(L.CADRE_SOCKET, cadre_attendu["socket"]); q(L.CADRE_PTR_NOM, cadre_attendu["ptr_nom"])
        if page != bytes(attendu):
            problemes.append("cadre hors prédiction octet par octet")
        for nom, valeur in SENTINELLES_NV.items():
            if self.uc.reg_read(REGS[nom]) != valeur:
                problemes.append(f"non-volatil {nom} modifié (I4)")
        for nom, rva in L.IAT_SEC32_SLOTS.items():
            if struct.unpack("<Q", bytes(self.uc.mem_read(rva, 8)))[0] != FAUX[nom]:
                problemes.append(f"IAT {nom} réécrite")
        if bytes(self.uc.mem_read(L.R_PKG_M4, len(L.PKG_M4))) != L.PKG_M4:
            problemes.append("fixture package altérée")
        return problemes

    def contrat_appels(self, appels_attendus: list[tuple]) -> list[str]:
        problemes = []
        if len(self.appels) != len(appels_attendus):
            problemes.append(f"trace d'appels {self.appels!r} != {appels_attendus!r}")
            return problemes
        for appel, (nom_att, off_att) in zip(self.appels, appels_attendus):
            nom = appel[0]
            if nom != nom_att:
                problemes.append(f"appel {nom} != {nom_att} (I1)")
                continue
            if nom == "ACH":
                (n, principal, pkg, usage, logonid, authdata, getkey,
                 getkeyarg, phcred, expiry, pkg_lu) = appel
                if principal != 0:
                    problemes.append(f"pszPrincipal {principal:#x} != NULL")
                if pkg != L.R_PKG_M4 or pkg_lu != L.PKG_M4:
                    problemes.append("pszPackage != fixture Schannel exacte")
                if usage != L.SECPKG_CRED_OUTBOUND:
                    problemes.append(f"fCredentialUse {usage} != OUTBOUND")
                if logonid != 0:
                    problemes.append(f"pvLogonId {logonid:#x} != NULL")
                if authdata != 0:
                    problemes.append(f"pAuthData {authdata:#x} != NULL (P3 : "
                                     "validation AUTOMATIQUE jamais désactivée)")
                if getkey != 0 or getkeyarg != 0:
                    problemes.append("pGetKeyFn/pvGetKeyArgument != NULL")
                if phcred != ZONE_CADRE + L.CADRE_CRED:
                    problemes.append(f"phCredential {phcred:#x} != cadre+0")
                if expiry != 0:
                    problemes.append(f"ptsExpiry {expiry:#x} != NULL")
            else:
                detail = appel[1]
                if detail != ZONE_CADRE + off_att:
                    problemes.append(f"{nom} handle {detail:#x} != cadre+{off_att:#x}")
        return problemes


# --- V2/V3 : différentiel --------------------------------------------------------

def jouer_cas(emu: Emulateur, op: int, hresult: int, magic: tuple[int, int],
              etiquette: str) -> tuple[list[str], int, int]:
    """Exécute UN cas contre le modèle — (écarts, verdict attendu, nb appels)."""
    cadre0 = cadre_initial()
    v_att, cadre_att, appels_att = modele_tls05(op, cadre0, hresult, magic)
    rax, cadre_lu = emu.executer(op, hresult, magic)
    problemes: list[str] = []
    if rax != v_att:
        problemes.append(f"verdict {rax} != {v_att} (modèle tls-02)")
    for champ in cadre_att:
        if cadre_lu[champ] != cadre_att[champ]:
            problemes.append(f"cadre.{champ} {cadre_lu[champ]:#x} != "
                             f"{cadre_att[champ]:#x}")
    problemes += emu.contrat_appels(appels_att)
    problemes += emu.hygiene(cadre_att)
    return problemes, v_att, len(emu.appels)


SCENARIOS_V2 = [
    ("acquisition succès", 0, 0x00000000, (0xA5A5A5A5A5A5A5A5, 0x5A5A5A5A5A5A5A5A)),
    ("acquisition échec certificat", 0, 0x80090325, (0, 0)),
    ("acquisition échec fatal", 0, 0x81234567, (0, 0)),
    ("acquisition verdict continuer (absurde, total)", 0, 0x00090312, (0, 0)),
    ("destruction succès", 1, 0x00000000, (0, 0)),
    ("destruction échec", 1, 0x80090308, (0, 0)),
    ("libération succès", 2, 0x00000000, (0, 0)),
    ("libération échec négocié", 2, 0x80090330, (0, 0)),
    ("opération hors domaine 3", 3, 0x00000000, (0, 0)),
    ("opération hors domaine 0xFFFFFFFF", 0xFFFFFFFF, 0x00000000, (0, 0)),
]

MUTATIONS_V4 = [
    ("M1 fCredentialUse INBOUND", ("mov r8d, 2", "mov r8d, 1")),
    ("M2 pAuthData non NULL (P3)", ("mov qword ptr [rsp + 0x20], 0",
                                    "mov qword ptr [rsp + 0x20], 1")),
    ("M3 zéro écrit sur la socket", ("mov qword ptr [rdx + 0x10], 0",
                                     "mov qword ptr [rdx + 0x20], 0")),
    ("M4 zéro d'échec sauté (op 0)", ("jz 0x6677", "jmp 0x6677")),
    ("M5 op 1 routée vers la libération", ("je 0x667c", "jne 0x667c")),
    ("M6 domaine relâché (op 3 accepté)", ("cmp ecx, 3", "cmp ecx, 4")),
]


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=5000)
    args = parseur.parse_args()
    rng = random.Random(args.graine)

    print("=== harnais_cles.py — tls-05:R1 (cycle de vie des handles, D81) ===")
    print(f"graine {args.graine} · fuzz {args.cas} cas")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # --- V1 : round-trip -------------------------------------------------------
    print("\n[V1] round-trip de notation")
    blob05, declare = octets_notation(ks, "tls-05-cles", RVA_TLS05)
    controle("tls-05-cles rassemblée == taille déclarée (Code : N o)",
             declare is not None and len(blob05) == declare,
             f"{len(blob05)} o")
    blob02, declare02 = octets_notation(ks, "tls-02-verdicts", RVA_TLS02)
    controle("tls-02-verdicts (intégration) == taille déclarée",
             declare02 is not None and len(blob02) == declare02, f"{len(blob02)} o")
    controle("padding du slot >= 16 (D8)", SLOT_TLS05 - len(blob05) >= 16,
             f"{SLOT_TLS05 - len(blob05)} o")

    # --- V2 : oracle à shims, scénarios de la spécification --------------------
    print("\n[V2] oracle à shims — scénarios de la spec (cadre octet par octet)")
    emu = Emulateur(blob05, blob02)
    for nom, op, hresult, magic in SCENARIOS_V2:
        problemes, v_att, n_appels = jouer_cas(emu, op, hresult, magic, nom)
        controle(f"scénario « {nom} »", not problemes,
                "; ".join(problemes[:3]) if problemes else
                f"verdict attendu {v_att}, {n_appels} appel(s)")

    # --- V3 : fuzzing à propriétés ----------------------------------------------
    print(f"\n[V3] fuzzing à propriétés — {args.cas} cas hostiles")
    codes_documentes = list(L.HRESULTS.keys())
    ecarts = 0
    for i in range(args.cas):
        if i % 4 == 3:
            op = rng.choice([3, 4, 5, 6, 7, 100, 0xFFFFFFFF, 0x80000000])
        else:
            op = rng.choice([0, 1, 2])
        if rng.random() < 0.6:
            hresult = rng.choice(codes_documentes)
        else:
            hresult = rng.getrandbits(32)
        magic = (rng.getrandbits(64), rng.getrandbits(64))
        problemes, _, _ = jouer_cas(emu, op, hresult, magic, "fuzz")
        if problemes:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart #{ecarts} op={op:#x} hresult={hresult:#x} : "
                      f"{'; '.join(problemes[:3])}")
    controle(f"fuzz {args.cas} cas : ZÉRO écart", ecarts == 0, f"{ecarts} écart(s)")

    # --- V4 : falsification ------------------------------------------------------
    print("\n[V4] falsification — six mutations d'un point, chacune attrapée")
    cas_mutants = [(0, 0x00000000, (1, 2)), (0, 0x80090325, (0, 0)),
                   (1, 0x00000000, (0, 0)), (2, 0x00000000, (0, 0)),
                   (3, 0x00000000, (0, 0)), (2, 0x8009030F, (0, 0)),
                   (0, 0x00090312, (0, 0))]
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "tls-05-cles", RVA_TLS05, mutation)
        emu_m = Emulateur(blob_m, blob02)
        attrapes = sum(1 for op, h, m in cas_mutants
                       if jouer_cas(emu_m, op, h, m, "mutant")[0])
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes}/{len(cas_mutants)} cas en écart")
    # témoin intact : le différentiel reste vert (une suite qui ne peut pas
    # échouer ne prouve rien — le témoin prouve que les pièges sont armés)
    emu_t = Emulateur(blob05, blob02)
    verts = sum(1 for op, h, m in cas_mutants
                if not jouer_cas(emu_t, op, h, m, "témoin")[0])
    controle("témoin intact : VERT sur les mêmes cas", verts == len(cas_mutants),
             f"{verts}/{len(cas_mutants)}")

    print("\n" + "=" * 70)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    print("=" * 70)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
