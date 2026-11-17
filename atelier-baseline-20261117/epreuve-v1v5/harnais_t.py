#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_t.py — L'ÉPREUVE D'EXÉCUTION V1-V5 DU BRAS T (le labo de la
baseline, session du 17/11/2026 — la suite prescrite du chantier : les
pièces sont LIVRÉES À L'ÉPREUVE, le harnais d'émulation Win32 la vit).

Le modèle : la pièce T cristallisée (376 o, preuves-baseline/cristal-T-07)
exécutée par unicorn aux ADRESSES DU PLAN — les QUATRE blocs tls13 scellés
assemblés à leurs slots (0xc000/0xc080/0xc240/0xc300, R7), la table K à
0x2f00 (le déplacement RIP de tls13-02), la zone d'état et TAMPON_CUMUL aux
cibles des lea de la pièce, l'IAT D161 servie par les shims du harnais
(SetFilePointerEx, ReadFile, GetLastError — la liste fermée).

Les vecteurs du contrat :
  V1 différentiel — proxy.exe scellé (la gamme entière + 1 000 gammes
     aléatoires, graine 20261117) + 100 gammes multi-fenêtres du témoin
     bi-fenêtre (proxy.exe ×2) contre hashlib.sha256 ;
  V2 doré — la gamme vide (e3b0c442…7852b855) et « abc » (ba7816bf…) ;
  V3 rejet — E1 session (-4), E2 hors-bornes (-3), E3 sortie nulle (-5) ;
  V4 rejet système — le shim ReadFile en échec à la 2e fenêtre : -6, la
     sortie INTACTE, le code consigné ;
  V5 falsification — un octet de TAMPON_CUMUL muté entre les fenêtres :
     le condensé DOIT diverger.

FALSIFIABLE : chaque verdict est dérivé de l'observation mécanique (les
octets, les registres, les adresses), jamais de la lecture du source. La
graine est consignée ; le rejeu est déterministe.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys

import capstone
import keystone
from unicorn import (Uc, UC_ARCH_X86, UC_MODE_64, UcError, UC_HOOK_CODE)
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_RAX, UC_X86_REG_RSP, UC_X86_REG_RBX,
                               UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15, UC_X86_REG_RIP)

ICI = os.path.dirname(os.path.abspath(__file__))
ATELIER = os.path.dirname(ICI)
SCELLES = os.path.join(ICI, "scelles")
REPO_TLS13 = "/home/z/my-project/triade/tls13"

# --- le plan d'adressage (les slots scellés de la famille, l'ère 1.0.0) --------
BASE_PIECE = 0x00401000          # la base de la cristallisation (cristalliser)
SLOT = {"tls13-01": (0xc000, 128), "tls13-02": (0xc080, 448),
        "tls13-03": (0xc240, 192), "tls13-04": (0xc300, 192)}
K_ADRESSE = 0x2f00               # le déplacement RIP de tls13-02 (0xc09d+7-0x91a4)
K_FIPS = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b,
          0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
          0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7,
          0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
          0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152,
          0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
          0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
          0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
          0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819,
          0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
          0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f,
          0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
          0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

# les adresses magiques du harnais (l'IAT pointe dessus, les shims y vivent)
SHIM_SETFILEPOINTEREX = 0x00010000
SHIM_READFILE = 0x00010008
SHIM_GETLASTERROR = 0x00010010
RETOUR_MAGIQUE = 0x00009000     # l'adresse de retour factice : l'exécution s'arrête
SORTIE_ADRESSE = 0x50000000     # le tampon de sortie de 32 o
PILE = 0x7FF000000000           # la pile du harnais
SESSION_HANDLE = 0x2000         # la valeur de poignée (opaque pour les shims)

FIPS_VIDE = bytes.fromhex("e3b0c44298fc1c149afbf4c8996fb924"
                          "27ae41e4649b934ca495991b7852b855")
FIPS_ABC = bytes.fromhex("ba7816bf8f01cfea414140de5dae2223"
                         "b00361a396177a9cb410ff61f20015ad")


def assembler_blocs_scelles() -> dict[str, bytes]:
    """les QUATRE notations scellées assemblées à leurs slots (keystone,
    les commentaires ôtés, le padding 0x90 au slot — la convention)."""
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    sortie = {}
    for nom in SLOT:
        chemin = os.path.join(SCELLES, f"{nom}-sha256-{ 'init' if nom=='tls13-01' else 'comprimer' if nom=='tls13-02' else 'absorber' if nom=='tls13-03' else 'finaliser'}.asm")
        lignes = []
        for l in open(chemin, encoding="utf-8"):
            l = l.split(";")[0].strip()
            if l:
                lignes.append(l)
        base, taille_slot = SLOT[nom]
        octets = b""
        addr = base
        for l in lignes:
            enc, _ = ks.asm(l, addr)
            octets += bytes(enc)
            addr += len(enc)
        assert len(octets) <= taille_slot, f"{nom} déborde son slot"
        sortie[nom] = octets + b"\x90" * (taille_slot - len(octets))
    return sortie


class HarnaisT:
    """la pièce T émulée : une instance par exécution (l'état est propre)."""

    def __init__(self, fichier: bytes):
        self.fichier = fichier
        self.taille = len(fichier)
        # la pièce cristallisée (l'itération COURANTE de la boucle § 5 :
        # T-07 le rejet consigné ; T-08 la reprise ; T-09 le courrier rbp
        # — le même harnais, la même graine, seule la pièce change)
        cristal = json.load(open(os.path.join(
            ATELIER, "preuves-baseline", "cristal-T-09.json"), encoding="utf-8"))
        assert cristal["vert"] and cristal["nb_octets"] == 394
        self.piece = bytes.fromhex(cristal["octets"])

        # les cibles des déplacements RIP — calculées par désassemblage
        cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cibles = {}
        for ins in cs.disasm(self.piece, BASE_PIECE):
            apres = ins.address + ins.size
            if ins.mnemonic == "lea" and "rbx" in ins.op_str and "rip" in ins.op_str:
                self.cibles["etat"] = apres + int(re.search(r"rip \+ (0x[0-9a-f]+)", ins.op_str).group(1), 16)
            elif ins.mnemonic == "lea" and "rdx" in ins.op_str and "rip" in ins.op_str:
                self.cibles["tampon"] = apres + int(re.search(r"rip \+ (0x[0-9a-f]+)", ins.op_str).group(1), 16)
            elif ins.mnemonic == "call" and "[rip" in ins.op_str:
                d = int(re.search(r"rip ([+-]) (0x[0-9a-f]+)", ins.op_str.replace("]", "")).group(2), 16)
                if re.search(r"rip - ", ins.op_str):
                    cible = apres - d
                else:
                    cible = apres + d
                if "etat" not in self.cibles or True:
                    self.cibles.setdefault("iat", []).append((ins.address, cible))
        # les TROIS slots IAT par ordre d'apparition : SetFilePointerEx, ReadFile, GetLastError
        self.iat = {"SetFilePointerEx": self.cibles["iat"][0][1],
                    "ReadFile": self.cibles["iat"][1][1],
                    "GetLastError": self.cibles["iat"][2][1]}

        # les réglages du vecteur (armés par l'épreuve avant l'appel)
        self.failread_au = None      # V4 : la fenêtre où ReadFile échoue
        self.mutate_au = None        # V5 : la fenêtre où TAMPON_CUMUL est muté
        self.derniere_erreur = 0
        self.fenetres_lues = 0
        self.journal_appels = []     # Q2 : la composition observée

    def _carter(self, page: int):
        self.uc.mem_map(page & ~0xFFF, 0x1000)

    def executer(self, decalage: int, longueur: int, session_valide=True,
                 sortie_nulle=False):
        """retourne {rax, sortie, crash, non_volatils, appels} — l'observation
        mécanique de l'exécution de la pièce."""
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.pos = 0
        self.fenetres_lues = 0
        self.derniere_erreur = 0
        self.journal_appels = []

        # --- la carte mémoire : K, les slots scellés, la pièce, l'IAT, les zones
        for page in (0x2000, 0xc000, BASE_PIECE):
            self._carter(page)
        self.uc.mem_write(K_ADRESSE, b"".join(k.to_bytes(4, "little") for k in K_FIPS))
        blocs = assembler_blocs_scelles()
        for nom, (base, _) in SLOT.items():
            self.uc.mem_write(base, blocs[nom])
        self.uc.mem_write(BASE_PIECE, self.piece)

        etat = self.cibles["etat"]
        tampon = self.cibles["tampon"]
        # les pages de la zone d'état (+528 → session, +520 → taille) et du tampon 64 Kio
        for zone, lon in ((etat, 0x300), (tampon, 0x11000)):
            p = zone & ~0xFFF
            npages = ((zone - p) + lon + 0xFFF) // 0x1000
            self.uc.mem_map(p, npages * 0x1000)
        self.uc.mem_write(etat + 520, self.taille.to_bytes(8, "little"))
        self.uc.mem_write(etat + 528,
                          (SESSION_HANDLE if session_valide else 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little"))
        # l'IAT : les TROIS slots pointent sur les shims
        iat_page = min(self.iat.values()) & ~0xFFF
        self.uc.mem_map(iat_page, 0x1000)
        self.uc.mem_write(self.iat["SetFilePointerEx"],
                          SHIM_SETFILEPOINTEREX.to_bytes(8, "little"))
        self.uc.mem_write(self.iat["ReadFile"], SHIM_READFILE.to_bytes(8, "little"))
        self.uc.mem_write(self.iat["GetLastError"], SHIM_GETLASTERROR.to_bytes(8, "little"))

        # les shims : des pages magiques vides (l'accroche y vit)
        self.uc.mem_map(SHIM_SETFILEPOINTEREX & ~0xFFF, 0x1000)
        self.uc.mem_map(RETOUR_MAGIQUE & ~0xFFF, 0x1000)
        # la sortie
        self.uc.mem_map(SORTIE_ADRESSE, 0x1000)
        avant_sortie = b"\xAA" * 32
        if not sortie_nulle:
            self.uc.mem_write(SORTIE_ADRESSE, avant_sortie)
        # la pile : 512 Kio, zéro-initiale (le contenu absorbé du créneau est
        # déterministe : des zéros sous la zone des arguments)
        self.uc.mem_map(PILE, 0x80000)
        rsp = PILE + 0x40000
        self.uc.mem_write(rsp - 0x100, b"\x00" * 0x100)

        # les non-volatils témoins (I5 : rendus ?)
        temoins = {r: 0x1111000 + i * 0x111 for i, r in enumerate(
            ("rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"))}
        regs = {"rbx": UC_X86_REG_RBX, "rbp": UC_X86_REG_RBP,
                "rdi": UC_X86_REG_RDI, "rsi": UC_X86_REG_RSI,
                "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13,
                "r14": UC_X86_REG_R14, "r15": UC_X86_REG_R15}

        # l'appel : l'adresse de retour magique posée, les arguments en place
        rsp -= 8
        self.uc.mem_write(rsp, RETOUR_MAGIQUE.to_bytes(8, "little"))
        self.uc.reg_write(UC_X86_REG_RSP, rsp)
        self.uc.reg_write(UC_X86_REG_RCX, decalage)
        self.uc.reg_write(UC_X86_REG_RDX, longueur)
        self.uc.reg_write(UC_X86_REG_R8, 0 if sortie_nulle else SORTIE_ADRESSE)
        for nom, r in regs.items():
            self.uc.reg_write(r, temoins[nom])

        # l'accroche des shims
        def au_code(uc, adresse, taille, donnees):
            if adresse == SHIM_SETFILEPOINTEREX:
                self.journal_appels.append("SetFilePointerEx")
                h = uc.reg_read(UC_X86_REG_RCX)
                off = uc.reg_read(UC_X86_REG_RDX)      # LARGE_INTEGER PAR VALEUR (msx64)
                assert h == SESSION_HANDLE, f"poignée inattendue {h:#x}"
                self.pos = off
                uc.reg_write(UC_X86_REG_RAX, 1)
                self._retour(uc)
            elif adresse == SHIM_READFILE:
                self.journal_appels.append("ReadFile")
                self.fenetres_lues += 1
                h = uc.reg_read(UC_X86_REG_RCX)
                dst = uc.reg_read(UC_X86_REG_RDX)
                n = uc.reg_read(UC_X86_REG_R8)
                assert h == SESSION_HANDLE
                if self.failread_au == self.fenetres_lues:
                    self.derniere_erreur = 5       # ERROR_ACCESS_DENIED, consigné
                    uc.reg_write(UC_X86_REG_RAX, 0)
                    self._retour(uc)
                    return
                a_lire = min(n, self.taille - self.pos)
                uc.mem_write(dst, self.fichier[self.pos:self.pos + a_lire])
                self.pos += a_lire
                if self.mutate_au == self.fenetres_lues:
                    mu = bytearray(uc.mem_read(dst, a_lire))
                    mu[0] ^= 0xFF                  # l'octet muté ENTRE les fenêtres
                    uc.mem_write(dst, bytes(mu))
                uc.reg_write(UC_X86_REG_RAX, 1)
                self._retour(uc)
            elif adresse == SHIM_GETLASTERROR:
                self.journal_appels.append("GetLastError")
                uc.reg_write(UC_X86_REG_RAX, self.derniere_erreur)
                self._retour(uc)

        self.uc.hook_add(UC_HOOK_CODE, au_code, begin=SHIM_SETFILEPOINTEREX & ~0xFFF,
                         end=(SHIM_SETFILEPOINTEREX & ~0xFFF) + 0xFFF)

        crash = None
        try:
            self.uc.emu_start(BASE_PIECE, RETOUR_MAGIQUE)
        except UcError as e:
            crash = f"{e} (rip={self.uc.reg_read(UC_X86_REG_RIP):#x})"
        rax = self.uc.reg_read(UC_X86_REG_RAX)
        if rax >= 1 << 63:
            rax -= 1 << 64
        sortie = bytes(self.uc.mem_read(SORTIE_ADRESSE, 32)) if not sortie_nulle else b""
        non_volatils = {nom: (self.uc.reg_read(r) == temoins[nom]) for nom, r in regs.items()}
        return {"rax": rax, "sortie": sortie.hex(),
                "sortie_intacte": sortie == avant_sortie,
                "crash": crash, "non_volatils": non_volatils,
                "appels": list(self.journal_appels),
                "fenetres": self.fenetres_lues}

    def _retour(self, uc):
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret = int.from_bytes(uc.mem_read(rsp, 8), "little")
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)


def epreuve():
    proxy = open(os.path.join(REPO_TLS13, "proxy.exe"), "rb").read()
    assert hashlib.sha256(proxy).hexdigest().startswith("446279f3")
    temoin_bi = proxy + proxy           # 130 048 o : DEUX fenêtres (V4, V5)
    graine = 20261117
    rng = random.Random(graine)
    gammes_proxy = [(0, len(proxy))]
    for _ in range(1000):
        off = rng.randint(0, len(proxy))
        lon = rng.randint(0, len(proxy) - off)
        gammes_proxy.append((off, lon))
    gammes_multi = []
    for _ in range(100):
        off = rng.randint(0, len(temoin_bi) - 65537)
        lon = rng.randint(65537, len(temoin_bi) - off)
        gammes_multi.append((off, lon))

    verdicts = {"bras": "T", "graine": graine, "vecteurs": {}}

    # ---- V1 : le différentiel
    h = HarnaisT(proxy)
    crashs = 0
    divergents = 0
    echantillon = []
    for i, (off, lon) in enumerate(gammes_proxy):
        r = h.executer(off, lon)
        attendu = hashlib.sha256(proxy[off:off + lon]).hexdigest()
        if r["crash"]:
            crashs += 1
        elif r["rax"] != 0 or r["sortie"] != attendu:
            divergents += 1
        if (r["crash"] or r["rax"] != 0 or r["sortie"] != attendu) and len(echantillon) < 6:
            echantillon.append({"cas": i, "gamme": [off, lon],
                                "crash": r["crash"], "rax": r["rax"],
                                "produit": r["sortie"][:16] + "…",
                                "attendu": attendu[:16] + "…"})
    h2 = HarnaisT(temoin_bi)
    for i, (off, lon) in enumerate(gammes_multi):
        r = h2.executer(off, lon)
        attendu = hashlib.sha256(temoin_bi[off:off + lon]).hexdigest()
        if r["crash"]:
            crashs += 1
        elif r["rax"] != 0 or r["sortie"] != attendu:
            divergents += 1
        if (r["crash"] or r["rax"] != 0 or r["sortie"] != attendu) and len(echantillon) < 6:
            echantillon.append({"cas": f"multi-{i}", "gamme": [off, lon],
                                "crash": r["crash"], "rax": r["rax"],
                                "produit": r["sortie"][:16] + "…",
                                "attendu": attendu[:16] + "…"})
    n = len(gammes_proxy) + len(gammes_multi)
    verdicts["vecteurs"]["V1"] = {
        "n": n, "crashs": crashs, "divergents": divergents,
        "echantillon": echantillon,
        "verdict": "ROUGE" if (crashs or divergents) else "VERT",
        "detail": (f"{crashs} crashs à l'exécution, {divergents} condensés "
                   f"divergents sur {n} gammes" if (crashs or divergents)
                   else "égalité octet par octet partout")}

    # ---- V2 : le doré
    h = HarnaisT(proxy)
    r_vide = h.executer(0, 0)
    abc_fichier = b"abc"
    h_abc = HarnaisT(abc_fichier)
    r_abc = h_abc.executer(0, 3)
    v2 = {"vide": {"produit": r_vide["sortie"], "attendu": FIPS_VIDE.hex(),
                   "ok": r_vide["sortie"] == FIPS_VIDE.hex() and r_vide["rax"] == 0},
          "abc": {"produit": r_abc["sortie"], "attendu": FIPS_ABC.hex(),
                  "ok": r_abc["sortie"] == FIPS_ABC.hex() and r_abc["rax"] == 0,
                  "crash": r_abc["crash"]}}
    v2["verdict"] = "VERT" if (v2["vide"]["ok"] and v2["abc"]["ok"]) else "ROUGE"
    verdicts["vecteurs"]["V2"] = v2

    # ---- V3 : les rejets
    h = HarnaisT(proxy)
    r_e1 = h.executer(0, 1, session_valide=False)
    r_e2 = h.executer(0, len(proxy) + 1)
    r_e3 = h.executer(0, 1, sortie_nulle=True)
    v3 = {"E1_session": {"rax": r_e1["rax"], "attendu": -4, "ok": r_e1["rax"] == -4},
          "E2_bornes": {"rax": r_e2["rax"], "attendu": -3, "ok": r_e2["rax"] == -3},
          "E3_entree": {"rax": r_e3["rax"], "attendu": -5, "ok": r_e3["rax"] == -5}}
    v3["verdict"] = "VERT" if all(v["ok"] for v in v3.values() if isinstance(v, dict)) else "ROUGE"
    verdicts["vecteurs"]["V3"] = v3

    # ---- V4 : le rejet système (ReadFile échoue à la 2e fenêtre)
    h = HarnaisT(temoin_bi)
    h.failread_au = 2
    r = h.executer(0, len(temoin_bi))
    v4 = {"rax": r["rax"], "attendu": -6, "ok_verdict": r["rax"] == -6,
          "sortie_intacte": r["sortie_intacte"], "ok_sortie": r["sortie_intacte"],
          "code_consigne": 5, "fenetres": r["fenetres"], "crash": r["crash"],
          "non_volatils": r["non_volatils"]}
    v4["verdict"] = "VERT" if (v4["ok_verdict"] and v4["ok_sortie"]) else "ROUGE"
    verdicts["vecteurs"]["V4"] = v4

    # ---- V5 : la falsification (TAMPON_CUMUL muté entre les fenêtres)
    h = HarnaisT(temoin_bi)
    r_ref = h.executer(0, len(temoin_bi))          # le condensé de référence (non muté)
    h = HarnaisT(temoin_bi)
    h.mutate_au = 2
    r_mut = h.executer(0, len(temoin_bi))          # le condensé muté
    if r_ref["crash"] or r_mut["crash"]:
        v5 = {"verdict": "ROUGE",
              "detail": "le condensé ne peut être observé — la pièce meurt "
                        "à la finalisation (crash), la falsification est "
                        "impossible à constater",
              "crash_ref": r_ref["crash"], "crash_mute": r_mut["crash"]}
    else:
        diverge = r_ref["sortie"] != r_mut["sortie"]
        v5 = {"produit_ref": r_ref["sortie"][:16] + "…",
              "produit_mute": r_mut["sortie"][:16] + "…",
              "divergence": diverge, "attendu": True,
              "verdict": "VERT" if diverge else "ROUGE"}
    verdicts["vecteurs"]["V5"] = v5

    # ---- les invariants observés (I5 : les non-volatils)
    h = HarnaisT(proxy)
    r = h.executer(0, 3)
    verdicts["invariants"] = {
        "I5_non_volatils_succes": r["non_volatils"],
        "I5_verdict": "VERT" if all(r["non_volatils"].values()) else "ROUGE",
        "Q2_appels_observes": r["appels"],
    }

    global_verdict = "CONFORME" if all(
        v["verdict"] == "VERT" for v in verdicts["vecteurs"].values()) else "REJET"
    verdicts["VERDICT"] = global_verdict
    return verdicts


if __name__ == "__main__":
    res = epreuve()
    sortie = os.path.join(ATELIER, "preuves-baseline", "epreuve-v1v5-bras-T.json")
    json.dump(res, open(sortie, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    print("\nécrit:", sortie)
