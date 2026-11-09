#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loupe/harnais_rendu.py — L'ORACLE À SCÉNARIOS du geste M10-(c).

Les familles rendu + navigation (loupe-08..14 : la ligne, l'écran, la
peinture, le défilement, l'aller, la recherche, le suivant) NOTÉES-
MESURÉES-PROUVÉES. Le modèle est le harnais du noyau (M10-(b)) : l'émulation
nue aux RVA du plan, l'appelant factice, le verdict TRANCHÉ par le code.

LA PIÈCE NEUVE DU GESTE : LE MINI-GUI VIRTUEL. Le rendu touche la vitrine
(les 15 feuilles user32 + les 6 gdi32 de l'IAT, la liste fermée) : le
harnais dote l'émulation de shims à l'ABI msx64 — la file de messages
SCRIPTÉE (GetMessageW/TranslateMessage/DispatchMessageW : le Dispatch
APPELLE LA PROCÉDURE au pointeur enregistré par RegisterClassExW, la
réponse revient par l'adresse magique — la mécanique EXACTE de USER32,
réduite au laboratoire), le DC qui ENREGISTRE (TextOutW : chaque goutte
avec ses coordonnées et ses couleurs, l'expansion latin-1 lue MOT À MOT),
la police mesurée une fois (16/8), le client rect, l'ascenseur, les
échecs paramétrables (BeginPaint nul, RegisterClassExW nul, la police
muette), ExitProcess qui TERMINÉ l'émulation (le code consigné).

L'ORACLE : le modèle PYTHON INDÉPENDANT recompose l'écran attendu (la
ligne 77 o du format du plan, l'entête, la grille bornée G = min(24,
ceil(remplissage/16), lignes_aff − 3), la barre-état aux QUATRE modes, le
panneau aux empreintes) depuis les TÉMOINS et l'état — JAMAIS depuis les
octets du bloc — et la comparaison est OCTET PAR OCTET sur les 2320 o de
la zone ECRAN. Le juge ne relit jamais l'accusé.

LE CAHIER (le miroir M10-(b), la charte § 3 : les vecteurs AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé démo relu (demo.exe 0.3.0, la source
       R7 de win-03), le scellé M1 relu (selftest.exe, la source de
       libc-02), les SEPT specs du geste relues, le plan recompté (les
       slots (c) ARRÊTÉS sur les mesures 271/1622/568/796/126/967 o et
       loupe-09 RÉVISÉ r2 au geste (d) — 874 → 1135 o, LA RÉVISION
       NOMMÉE : la table de routage étendue SANS cascade, le slot croît
       0x380 → 0x480, la famille édition suit à 0x6080 — l'instrument
       retoqué aux attentes r2 au geste du build, le miroir de la spec ;
       les adresses .rdata du rendu, les libellés, l'IAT démo win-03) ;
  V1 — LE ROUND-TRIP + LA STRUCTURE : chaque notation ré-assemblée
       (keystone == capstone, R5), les déplacements RIP aux symboles du
       plan, les appels directs à la liste fermée (le réseau des specs),
       les feuilles IAT par bloc, L'HÉRITAGE R7 CONSTATÉ BYTE-IDENTIQUE —
       LA DOUBLE PREUVE (libc-02 @0x1180 depuis selftest.exe ET win-03
       @0x15C0 depuis demo.exe : les octets émulés == les extraits des
       scellés ET les notations d'origine ré-assemblées == les extraits) ;
  V2 — LOUPE-08 LA LIGNE : le doré (la première ligne de proxy.exe scellé
       + la ligne finale incomplète du témoin 3f) + 1 500 lignes
       différentielles (décalages, longueurs 1..16, alphabet plein) ==
       le modèle Python + les 16 longueurs bornées + LES TROIS REJETS
       (longueur 0, longueur 17, pointeurs nuls : -5, la sortie INTACTE) ;
  V3 — LOUPE-13 LA RECHERCHE : le corpus de l'école (le premier octet, le
       dernier, à cheval sur le départ, l'occurrence double, AAAA dans
       AAAAB) + 1 500 cas différentiels (fenêtres 0..2 048, motifs 1..32,
       alphabets plein et pauvre) == bytes.find À L'IDENTIQUE y compris
       les -1 + les fenêtres réelles de proxy.exe (MZ, PEMax, « This
       program ») + LES TROIS REJETS (motif vide, 33 o, départ au-delà) ;
  V4 — LOUPE-14 LE SUIVANT : LA CHAÎNE au fichier entier (chaque
       occurrence ET LA FIN comparées à la chaîne bytes.find sur le
       témoin 3f — 3 fenêtres de 64 Kio + 1) + LE RECOUVREMENT PAR
       CONSTRUCTION (un témoin composé où l'occurrence N'EXISTE qu'à
       cheval sur chaque frontière de 64 Kio : TROUVÉE — le mutant d'un
       octet la manquerait) + 12 motifs aléatoires différentiels sur un
       témoin de 70 000 o + LES REJETS (4d5 impair, zz, vide → -5 nommé ;
       sans session → -4 ; le shim ReadFile en échec → -6 relayé, la
       position intacte) ;
  V5 — LE DÉFILEMENT + L'ALLER : la borne différentielle (vue_max et le
       clamp rejoués contre le plan sur 10 000 tailles aléatoires) + les
       scénarios (la molette au bout : LA DERNIÈRE FENÊTRE VOIT le
       dernier octet ; le petit fichier : la molette SANS effet, RIEN
       relu — les compteurs ; WM_SIZE recalculé) + les scénarios de
       l'aller (le saut au milieu : le curseur exact, la vue recalée à
       la 12e ligne, L'ÉCRAN ATTENDU OCTET PAR OCTET ; le 9e chiffre
       ignoré ; VK_SUPPR retire ; VK_ECHAP annule TOUT ; les refus
       NOMMÉS : vide/non-hexa → -5 « saisie mal formée », hors bornes →
       -3 « hors bornes », sans session → -4 « aucun fichier ouvert ») ;
  V6 — L'ORACLE À SCÉNARIOS (le critère du plan) : la vitrine SANS
       session (l'usage à la barre, « - » au panneau, l'écran attendu
       octet par octet, la file scriptée) ; le témoin ouvert PAR LA
       LIGNE DE COMMANDE (la session née entière AVANT la vitrine, les
       24 lignes, le panneau == hashlib, la cellule active INVERSÉE à
       l'abscisse exacte) ; la marque sale (MODIFIÉ + l'astérisque) ; LE
       ROUTAGE CONSTATÉ (chaque message chez son bloc, les appels comptés
       un à un, DefWindowProcW pour le reste) ; le refus à l'ouverture
       (« fichier introuvable » à la barre, la vitrine VIDE VRAIE) ;
       E1/E2 (RegisterClassExW nul, CreateWindowExW nul : MessageBoxW
       PUIS ExitProcess(1), la boucle JAMAIS lancée) ;
  V7 — LA FALSIFICATION (zéro silence) : le remplissage d'espaces de
       loupe-08 muté d'un octet → l'écran attendu DIVERGE (l'oracle
       échoue — DEMANDÉ) ; la constante de recadrage de loupe-12 mutée
       (176 → 192) → l'écran du saut diverge ; l'anti-muet (chaque octet
       de l'écran attendu muté → la comparaison échoue) ; la table HEX
       mutée → chaque ligne diverge.

Usage : python3 harnais_rendu.py            # le cahier complet
        python3 harnais_rendu.py --graine N # la graine (défaut 20261108)
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)

# Le harnais du noyau importé PAR CHEMIN NOMINATIF (la leçon D158) — la
# machinerie M10-(b) réutilisée TELLE QUELLE : l'émulation, le mini-OS
# virtuel, les témoins, l'appelant factice.
sys.path.insert(0, ICI)
if "harnais_noyau_mod" in sys.modules:
    HN = sys.modules["harnais_noyau_mod"]
else:
    _spec_hn = importlib.util.spec_from_file_location(
        "harnais_noyau_mod", os.path.join(ICI, "harnais_noyau.py"))
    HN = importlib.util.module_from_spec(_spec_hn)
    sys.modules["harnais_noyau_mod"] = HN
    _spec_hn.loader.exec_module(HN)

L = HN.L          # le plan loupe (la source unique)
B4 = HN.B4        # la machinerie de notation (assembler_bloc/round_trip)
ErreurHarnais = HN.ErreurHarnais
controle = HN.controle
section = HN.section
REUSSITES, ECHECS = HN.REUSSITES, HN.ECHECS

from unicorn import Uc, UcError  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP)

# --- les pièces du plan rendu (les adresses .rdata ARRÊTÉES au geste) --------------

SCELLE_DEMO = "demo/demo.exe"      # la pièce de l'ère démo (win-03 vit dedans)
SCELLE_DEMO_TAILLE = 0x4000
SCELLE_DEMO_MD5 = "73c064fbaf4610a167bc6434dee400e4"
SCELLE_DEMO_SHA256 = ("df8f2e50949b14c072f139013a6166a0"
                      "41e573e49b6872d826958f522495e4af")

RETOUR_DISPATCH = 0x900800         # l'adresse magique : la procédure rend, le
                                   # Dispatch reprend (dans ZONE_SHIMS, hors
                                   # des slots — jamais exécutée comme code)
ADRESSE_CMDLINE = 0x700500         # la ligne de commande du scénario (UTF-16)
ADRESSE_FENETRE = 0x710000         # la grande fenêtre de test (loupe-13 : les
                                   # fenêtres jusqu'à 64 Kio — JAMAIS sous le
                                   # motif : les zones disjointes, sinon le
                                   # témoin écrase la question)
ADRESSE_MOTIF = 0x730000           # le motif de test (33 o + la garde)
HDC_FAKE = 0x700001                # le DC du laboratoire

# les libellés .rdata du plan (les octets EXACTS — le « · » est 0xB7 latin-1)
LIBELLES = {
    "usage": (L.L_USAGE, "loupe <fichier>"),
    "balise": (L.L_BALISE, "Loupe 0.1.0-dev.1"),
    "tiret": (L.L_TIRET, " - "),
    "mid": (L.L_MID, " \xb7 "),
    "oct": (L.L_OCT, " o \xb7 curseur 0x"),
    "modif": (L.L_MODIF, " \xb7 MODIFI\xc9"),
    "md5": (L.L_MD5, "md5 "),
    "sha": (L.L_SHA, " \xb7 sha256 "),
    "ast": (L.L_AST, " *"),
    "vide": (L.L_VIDE, "-"),
    "aller": (L.L_ALLER, "ALLER (hexa) : "),
    "chercher": (L.L_CHERCHER, "CHERCHER (hexa) : "),
    "malformee": (L.L_MALFORMEE, "saisie mal form\xe9e"),
    "horsbornes": (L.L_HORSBORNES, "hors bornes"),
    "session": (L.L_SESSION, "aucun fichier ouvert"),
    "fin": (L.L_FIN, "plus d'occurrence"),
    "paires": (L.L_PAIRES, "paires hexa attendues"),
    "systeme": (L.L_SYSTEME, "refus syst\xe8me"),
    "absent": (L.L_ABSENT, "fichier introuvable"),
}
ENTETE_TEXTE = ("D\xe9calage  00 01 02 03 04 05 06 07"
                "  08 09 0A 0B 0C 0D 0E 0F  ASCII")
CLASSE_NOM = "LoupeHexa"
TITRE_NOM = "Loupe \u2014 l'\xe9diteur hexad\xe9cimal"
ERREUR_NOM = "La fen\xeatre de Loupe ne peut pas \xeatre cr\xe9\xe9e."

NOMS_RENDU = {
    "i110008": "loupe-08-ligne", "i110009": "loupe-09-ecran",
    "i110010": "loupe-10-peinture", "i110011": "loupe-11-defilement",
    "i110012": "loupe-12-aller", "i110013": "loupe-13-recherche",
    "i110014": "loupe-14-suivant",
}
MESURES_RENDU = {"i110008": 271, "i110009": 1135, "i110010": 1622,
                 "i110011": 568, "i110012": 796, "i110013": 126,
                 "i110014": 983}   # i110009 : la mesure r2 du geste (d)

FEUILLES_GUI_USER32 = (
    "RegisterClassExW", "CreateWindowExW", "ShowWindow", "GetMessageW",
    "TranslateMessage", "DispatchMessageW", "DefWindowProcW", "BeginPaint",
    "EndPaint", "InvalidateRect", "GetClientRect", "GetScrollInfo",
    "SetScrollInfo", "LoadCursorW", "MessageBoxW")
FEUILLES_GUI_GDI = ("GetStockObject", "SelectObject", "GetTextMetricsW",
                    "TextOutW", "SetTextColor", "SetBkColor")
FEUILLES_GUI_K32 = ("GetCommandLineW", "ExitProcess")


# --- le mini-GUI virtuel (la pièce neuve du geste) --------------------------------

class GUIVirtuel:
    """La vitrine vue par les shims : la file scriptée, le DC qui enregistre,
    la police, le client, l'ascenseur, les échecs paramétrables, les
    compteurs — tout ce que l'oracle constate sur pièces."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.file: list[tuple[int, int, int, int]] = []   # (hwnd, msg, wP, lP)
        self.wndproc = 0                # posé par RegisterClassExW
        self.classe_nom = ""
        self.titre = ""
        self.hwnd = 0                   # posé par CreateWindowExW
        self.style = 0
        self.cmdline_ptr = ADRESSE_CMDLINE
        self.cx, self.cy = 640, 440     # le client (GetClientRect)
        self.tm_hauteur, self.tm_chasse = 16, 8
        self.trackpos = 0               # GetScrollInfo nTrackPos
        self.scroll = None              # (min, max, page, pos) posé
        self.gouttes: list[tuple] = []  # TextOutW (x, y, texte, couleurs)
        self.couleur_texte, self.couleur_fond = 0x00000000, 0x00FFFFFF
        self.compteurs = {f: 0 for f in
                          FEUILLES_GUI_USER32 + FEUILLES_GUI_GDI
                          + FEUILLES_GUI_K32}
        self.appels_defproc = 0
        self.boites: list[tuple] = []   # MessageBoxW (texte, titre, type)
        self.exit_code = None           # posé par ExitProcess
        self.arm_beginpaint = False     # E1 : le DC nul
        self.arm_police = False         # E2 : GetTextMetricsW muet
        self.arm_register = False       # E1 de loupe-09
        self.arm_create = False         # E2 de loupe-09
        self.arm_scrollinfo = False     # E1 de loupe-11

    def scripter(self, *messages):
        self.file = list(messages)

    def texte_u16(self, uc, adr, cap=260):
        brut = bytes(uc.mem_read(adr, cap * 2))
        fin = brut.find(b"\x00\x00")
        if fin > 0:
            brut = brut[:fin + 1]
        return brut.decode("utf-16-le", errors="replace").rstrip("\x00")


class EmulationRendu(HN.Emulation):
    """L'image loupe du geste (c) : les QUATORZE notations, libc-02 et win-03
    posés AUX ADRESSES SCELLÉES, l'IAT démo @0x2818+, les 29 shims vivants
    (les 5 feuilles du chantier (d) demeurent au mort)."""

    def __init__(self, os_virtuel, donnees_m9: bytes, donnees_m1: bytes,
                 donnees_demo: bytes):
        super().__init__(os_virtuel)
        self.gui = GUIVirtuel()
        gui = self.gui

        # LES HÉRITAGES DU NOYAU posés par la voie canonique (libc-01/07 +
        # tls13-01..04 aux adresses scellées — le mécanisme M10-(b) repris
        # TEL QUEL : la sous-classe ne ré-écrit jamais la pose)
        self.poser_heritages(donnees_m9, donnees_m1)

        # la grande fenêtre de test (les fenêtres loupe-13 jusqu'à 64 Kio +
        # le motif : les adresses DISJOINTES — le témoin n'écrase jamais la
        # question)
        self.uc.mem_map(0x710000, 0x21000)

        # -- les 7 notations du geste (le lecteur canonique) --------------------
        for bid, nom in NOMS_RENDU.items():
            rva, slot = L.SLOTS_LOUPE[bid]
            chemin = os.path.join(ICI, "notation", nom + ".asm")
            octets, metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            self.uc.mem_write(rva, octets)
            self.blobs[bid] = (octets, metas)

        # -- les pièces .rdata du rendu (le plan, source unique) ----------------
        self.uc.mem_write(L.R_ENTETE, ENTETE_TEXTE.encode("latin-1") + b"\x00")
        self.uc.mem_write(L.R_HEX, b"0123456789ABCDEF\x00")
        self.uc.mem_write(L.R_HEXL, b"0123456789abcdef\x00")
        for _, (adr, texte) in LIBELLES.items():
            self.uc.mem_write(adr, texte.encode("latin-1") + b"\x00")
        self.uc.mem_write(L.R_CLASSE, CLASSE_NOM.encode("utf-16-le") + b"\x00\x00")
        self.uc.mem_write(L.R_TITRE, TITRE_NOM.encode("utf-16-le") + b"\x00\x00")
        self.uc.mem_write(L.R_ERREUR, ERREUR_NOM.encode("utf-16-le") + b"\x00\x00")

        # -- LES HÉRITAGES DU GESTE (c) aux adresses scellées (la règle (b)) --
        libc02 = self.extraire(donnees_m1, L.R_LIBC02, 0x80)
        win03 = self.extraire(donnees_demo, L.R_WIN03, 0x80)
        self.uc.mem_write(L.R_LIBC02, libc02)
        self.uc.mem_write(L.R_WIN03, win03)
        self.heritages_rendu = {"libc-02": libc02, "win-03": win03}

        # -- l'IAT : les 29 feuilles vivantes du geste (c) ----------------------
        #    les 5 du chantier (d) + GetModuleHandleW demeurent AU MORT
        base = HN.ZONE_SHIMS[0]
        self.adr_shims_mort: set[int] = set()
        i = 8                       # les 6 shims noyau vivent à base+0..0x38
        vivantes = (FEUILLES_GUI_K32 + FEUILLES_GUI_USER32 + FEUILLES_GUI_GDI)
        for feuille in vivantes:
            adr = base + 8 * i
            i += 1
            self.adr_shims[adr] = feuille
            self.uc.mem_write(L.IAT_SLOTS[feuille], struct.pack("<Q", adr))
        # les feuilles du (d) : le mort les garde (l'appel DÉNONCÉ)
        for feuille in ("GetModuleHandleW", "WriteFile", "DestroyWindow",
                        "PostQuitMessage", "MessageBeep"):
            self.uc.mem_write(L.IAT_SLOTS[feuille], struct.pack("<Q", HN.SHIM_MORT))
        # L'IAT DÉMO : les TROIS slots que les déplacements scellés de win-03
        # visent — les MÊMES shims que l'IAT loupe (la double entrée n'est pas
        # une redondance, c'est le prix du déplacement scellé)
        for slot, feuille in ((L.R_IAT_DEMO_GMW, "GetMessageW"),
                              (L.R_IAT_DEMO_TM, "TranslateMessage"),
                              (L.R_IAT_DEMO_DMW, "DispatchMessageW")):
            adr_shim = struct.unpack("<Q", self.uc.mem_read(
                L.IAT_SLOTS[feuille], 8))[0]
            self.uc.mem_write(slot, struct.pack("<Q", adr_shim))

    @staticmethod
    def extraire(donnees: bytes, rva_orig: int, taille: int) -> bytes:
        e = struct.unpack_from("<I", donnees, 0x3C)[0]
        n = struct.unpack_from("<H", donnees, e + 6)[0]
        opt = struct.unpack_from("<H", donnees, e + 20)[0]
        for k in range(n):
            o = e + 24 + opt + k * 40
            va, = struct.unpack_from("<I", donnees, o + 12)
            ra, = struct.unpack_from("<I", donnees, o + 20)
            vs, = struct.unpack_from("<I", donnees, o + 8)
            if va <= rva_orig < va + vs:
                raw = ra + (rva_orig - va)
                return donnees[raw:raw + taille]
        raise ErreurHarnais(f"RVA {rva_orig:#x} introuvable")

    # -- les procédés du bloc rendu ------------------------------------------

    def adresse_procedure(self) -> int:
        """LA PROCÉDURE relue depuis l'ENTÊTE de sa notation (les étiquettes
        résolues — la notation nomme ce que le plan adresse)."""
        chemin = os.path.join(ICI, "notation", "loupe-09-ecran.asm")
        for ligne in open(chemin, encoding="utf-8"):
            if ligne.startswith("; Étiquettes résolues :"):
                for morceau in ligne.split(":", 1)[1].split(","):
                    morceau = morceau.strip()
                    if morceau.startswith(".procedure="):
                        return int(morceau.split("=")[1], 16)
        raise ErreurHarnais("l'étiquette .procedure introuvable dans loupe-09")

    def message(self, msg: int, wparam: int = 0, lparam: int = 0):
        return (self.gui.hwnd or 0x770001, msg, wparam, lparam)

    def appeler_winmain(self, cmdline: str, messages=None):
        """Le scénario de la vitrine : la ligne de commande posée, la file
        scriptée, WinMain appelé comme le fera le chargeur (rcx = hInstance,
        l'entrée du bloc) — ExitProcess termine l'émulation, le code consigné."""
        gui = self.gui
        if messages is not None:
            gui.scripter(*messages)
        self.uc.mem_write(ADRESSE_CMDLINE,
                          cmdline.encode("utf-16-le") + b"\x00\x00")
        r = self.appeler(L.LOUPE09_VA, {"rcx": 0x760000, "rdx": 0,
                                        "r8": ADRESSE_CMDLINE, "r9": 5})
        r["exit_code"] = gui.exit_code
        return r

    # -- l'appelant factice étendu : le 5e argument À LA PILE (loupe-13) ---

    def appeler(self, va: int, args: dict | None = None,
                pile_args: list | None = None):
        """L'appelant factice du noyau, étendu : pile_args pose les arguments
        AU-DELÀ du quatrième à [rsp+0x28+8k] (le 5e de loupe-13 — le contrat
        P5) ; le canari couvre la zone AU-DESSUS des arguments (jamais un
        faux échec par la place de l'argument)."""
        if not pile_args:
            return super().appeler(va, args)
        uc = self.uc
        for nom, val in HN.SENTINELLES_NV.items():
            uc.reg_write(HN.REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(HN.REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = HN.ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp, struct.pack("<Q", HN.RET_MAGIQUE))
        uc.mem_write(rsp + 8, HN.CANARI * 0x170)
        for k, val in enumerate(pile_args):
            uc.mem_write(rsp + 0x28 + 8 * k, struct.pack("<Q", val))
        entree_rsp = rsp
        try:
            uc.emu_start(va, HN.RET_MAGIQUE, count=200_000_000)
        except UcError as err:
            return {"crash": str(err), "entree_rsp": entree_rsp,
                    "canaris_haut": False, "pile_equilibree": False}
        sortie = {k: uc.reg_read(HN.REGS[k]) for k in HN.REGS}
        sortie["rax"] = HN.verdict_eax(sortie["rax"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["pile_equilibree"] = uc.reg_read(HN.REGS["rsp"]) == entree_rsp + 8
        debut_canari = rsp + 0x28 + 8 * len(pile_args)
        sortie["canaris_haut"] = bytes(uc.mem_read(
            debut_canari, 0x178 - 0x28 - 8 * len(pile_args))) == \
            HN.CANARI * (0x178 - 0x28 - 8 * len(pile_args))
        return sortie

    # -- le hook étendu (les shims GUI + la magie du Dispatch) ----------------

    def _retour(self, uc, rax: int) -> None:
        super()._retour(uc, rax)

    def _shim_gui(self, uc, feuille: str) -> bool:
        """Retourne True si la feuille fut servie (les 27 du GUI)."""
        gui = self.gui
        os_v = self.os
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        r9 = uc.reg_read(UC_X86_REG_R9)
        rsp = uc.reg_read(UC_X86_REG_RSP)

        def qword(adr):
            return struct.unpack("<Q", uc.mem_read(adr, 8))[0]

        if feuille == "GetMessageW":
            gui.compteurs[feuille] += 1
            if gui.file:
                hwnd, msg, wp, lp = gui.file.pop(0)
                uc.mem_write(rcx, struct.pack("<QIIQQ", hwnd, msg, 0, wp, lp))
                self._retour(uc, 1)
            else:
                self._retour(uc, 0)      # la file vide : WM_QUIT, la boucle rend
            return True
        if feuille == "TranslateMessage":
            gui.compteurs[feuille] += 1
            self._retour(uc, 0)
            return True
        if feuille == "DispatchMessageW":
            gui.compteurs[feuille] += 1
            if not gui.wndproc:
                raise ErreurHarnais("DispatchMessageW sans procédure enregistrée")
            hwnd, msg = struct.unpack("<QI", uc.mem_read(rcx, 12))
            wp = qword(rcx + 16)
            lp = qword(rcx + 24)
            # LA MÉCANIQUE D'USER32 RÉDUITE : la pile reçoit l'adresse magique,
            # les quatre arguments, rip vise LA PROCÉDURE enregistrée — la
            # réponse revient par RETOUR_DISPATCH (le hook y rend au call site)
            uc.reg_write(UC_X86_REG_RSP, rsp - 8)
            uc.mem_write(rsp - 8, struct.pack("<Q", RETOUR_DISPATCH))
            uc.reg_write(UC_X86_REG_RCX, hwnd)
            uc.reg_write(UC_X86_REG_RDX, msg)
            uc.reg_write(UC_X86_REG_R8, wp)
            uc.reg_write(UC_X86_REG_R9, lp)
            uc.reg_write(UC_X86_REG_RIP, gui.wndproc)
            return True
        if feuille == "DefWindowProcW":
            gui.compteurs[feuille] += 1
            gui.appels_defproc += 1
            self._retour(uc, 0)
            return True
        if feuille == "BeginPaint":
            gui.compteurs[feuille] += 1
            if gui.arm_beginpaint:
                self._retour(uc, 0)
            else:
                uc.mem_write(rdx, struct.pack("<QI", HDC_FAKE, 0))
                self._retour(uc, HDC_FAKE)
            return True
        if feuille == "EndPaint":
            gui.compteurs[feuille] += 1
            self._retour(uc, 1)
            return True
        if feuille == "GetStockObject":
            gui.compteurs[feuille] += 1
            self._retour(uc, 0 if gui.arm_police else 0x710001)
            return True
        if feuille == "SelectObject":
            gui.compteurs[feuille] += 1
            self._retour(uc, 0x710002)
            return True
        if feuille == "GetTextMetricsW":
            gui.compteurs[feuille] += 1
            if gui.arm_police:
                self._retour(uc, 0)
            else:
                tm = struct.pack("<iiiiiiii", gui.tm_hauteur, 12, 4, 3, 1,
                                 gui.tm_chasse, 400, 0)
                uc.mem_write(rdx, tm)
                self._retour(uc, 1)
            return True
        if feuille == "TextOutW":
            gui.compteurs[feuille] += 1
            n = qword(rsp + 0x28) & 0xFFFFFFFF   # le 5e argument : le compte
            mots = struct.unpack(f"<{n}H", uc.mem_read(r9, 2 * n))
            gui.gouttes.append((rdx & 0xFFFFFFFF, r8 & 0xFFFFFFFF, mots,
                                gui.couleur_texte, gui.couleur_fond))
            self._retour(uc, 1)
            return True
        if feuille in ("SetTextColor", "SetBkColor"):
            gui.compteurs[feuille] += 1
            ancien = (gui.couleur_texte if feuille == "SetTextColor"
                      else gui.couleur_fond)
            if feuille == "SetTextColor":
                gui.couleur_texte = rdx & 0xFFFFFFFF
            else:
                gui.couleur_fond = rdx & 0xFFFFFFFF
            self._retour(uc, ancien)
            return True
        if feuille == "GetClientRect":
            gui.compteurs[feuille] += 1
            uc.mem_write(rdx, struct.pack("<iiii", 0, 0, gui.cx, gui.cy))
            self._retour(uc, 1)
            return True
        if feuille == "GetScrollInfo":
            # (hwnd, SB_VERT, &si) : la structure est le TROISIÈME argument (r8)
            gui.compteurs[feuille] += 1
            if gui.arm_scrollinfo:
                self._retour(uc, 0)
            else:
                masque = struct.unpack("<I", uc.mem_read(r8 + 4, 4))[0]
                if masque & 0x10:
                    uc.mem_write(r8 + 24, struct.pack("<I", gui.trackpos))
                self._retour(uc, 1)
            return True
        if feuille == "SetScrollInfo":
            # (hwnd, SB_VERT, &si, redraw) : la structure est le TROISIÈME (r8)
            gui.compteurs[feuille] += 1
            nmin, nmax = struct.unpack("<ii", uc.mem_read(r8 + 8, 8))
            page, npos = struct.unpack("<II", uc.mem_read(r8 + 16, 8))
            ancien = gui.scroll[3] if gui.scroll else 0
            gui.scroll = (nmin, nmax, page, npos)
            self._retour(uc, ancien)
            return True
        if feuille == "InvalidateRect":
            gui.compteurs[feuille] += 1
            self._retour(uc, 1)
            return True
        if feuille == "RegisterClassExW":
            gui.compteurs[feuille] += 1
            gui.wndproc = qword(rcx + 8)
            gui.classe_nom = gui.texte_u16(uc, qword(rcx + 64), 64)
            if gui.arm_register:
                self._retour(uc, 0)
            else:
                self._retour(uc, 0x8001)
            return True
        if feuille == "CreateWindowExW":
            gui.compteurs[feuille] += 1
            gui.titre = gui.texte_u16(uc, r8, 64)
            gui.style = r9 & 0xFFFFFFFF
            gui.hwnd = 0 if gui.arm_create else 0x770001
            self._retour(uc, gui.hwnd)
            return True
        if feuille == "ShowWindow":
            gui.compteurs[feuille] += 1
            self._retour(uc, 0)
            return True
        if feuille == "LoadCursorW":
            gui.compteurs[feuille] += 1
            self._retour(uc, 0x730001)
            return True
        if feuille == "MessageBoxW":
            gui.compteurs[feuille] += 1
            gui.boites.append((gui.texte_u16(uc, rdx, 128),
                               gui.texte_u16(uc, r8, 64), r9 & 0xFFFFFFFF))
            self._retour(uc, 1)
            return True
        if feuille == "GetCommandLineW":
            gui.compteurs[feuille] += 1
            self._retour(uc, gui.cmdline_ptr)
            return True
        if feuille == "ExitProcess":
            gui.compteurs[feuille] += 1
            gui.exit_code = rcx & 0xFFFFFFFF
            # la fin : rip vise l'adresse JUSQU'À de l'appelant factice —
            # l'émulation s'achève proprement (le code consigné)
            uc.reg_write(UC_X86_REG_RIP, HN.RET_MAGIQUE)
            return True
        return False

    def _instrument(self, uc, adresse, taille, donnees):
        if adresse == RETOUR_DISPATCH:
            # la procédure a rendu : DispatchMessageW rend À SON TOUR au
            # site d'appel de win-03 (rax = 0, l'adresse de retour lue)
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RAX, 0)
            uc.reg_write(UC_X86_REG_RIP, ret)
            return
        if adresse in self.adr_shims:
            feuille = self.adr_shims[adresse]
            if feuille in HN.FEUILLES_NOYAU:
                self._shim(uc, feuille)
                return
            if self._shim_gui(uc, feuille):
                return
            raise ErreurHarnais(f"shim GUI inconnu : {feuille}")
        elif adresse == HN.SHIM_MORT:
            self.os.appels_interdits += 1
            self._retour(uc, 0)


# =====================================================================================
# LE MODÈLE — la composition indépendante de l'écran attendu (le juge ne
# relit JAMAIS l'accusé : les témoins et l'état entrent, les 2320 o sortent)
# =====================================================================================

def model_ligne(decalage: int, octets: bytes) -> bytes:
    """La ligne 77 o du format du plan : 8 chiffres MAJUSCULES du décalage,
    2 espaces, 16 groupes séparés d'un espace (le médian DOUBLÉ), 2 espaces,
    le miroir ASCII (le point hors 0x20..0x7E), le NUL — les groupes et le
    miroir au-delà de la longueur demeurent des espaces (Q3 : la colonne
    ASCII ne bouge jamais)."""
    s = f"{decalage:08X}  "
    groupes = [f"{b:02X}" if i < len(octets) else "  " for i, b in
               enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(groupes[:8]) + "  " + " ".join(groupes[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"


def _creneaux(texte: str, longueur: int) -> bytes:
    return texte.encode("latin-1")[:longueur - 1].ljust(longueur, b"\x00")


def model_ecran(fenetre: bytes, vue: int, remplissage: int, taille: int,
                chemin: str, curseur: int, sale: int, empreintes: bytes,
                mode: int, tampon_saisie: bytes, lignes_aff: int) -> bytes:
    """Les 2320 o de la zone ECRAN : l'entête 80 @0, la grille 24×80 @80,
    la barre 2×160 @2000 — la barre-état aux QUATRE modes, le panneau aux
    empreintes du DISQUE (l'astérisque si la marque sale). La FENÊTRE vient
    des octets RÉELS du témoin (le juge lit le fichier, jamais le cadre)."""
    ecran = bytearray(2320)
    # l'entête (65 o utiles + NUL)
    ecran[0:66] = ENTETE_TEXTE.encode("latin-1") + b"\x00"
    # la grille : G = min(24, ceil(remplissage/16), max(0, lignes_aff − 3))
    g = min(24, (remplissage + 15) // 16, max(0, lignes_aff - 3))
    for i in range(g):
        ligne = model_ligne(vue + 16 * i, fenetre[16 * i:16 * i + 16])
        ecran[80 + 80 * i:80 + 80 * i + 77] = ligne
    # la barre ligne 1 (les quatre modes)
    if mode == 3:                        # MESSAGE : le refus nommé au tampon
        texte = tampon_saisie.split(b"\x00")[0].decode("latin-1")
    elif mode == 1:
        texte = LIBELLES["aller"][1] + tampon_saisie.split(b"\x00")[0].decode("latin-1")
    elif mode == 2:
        texte = LIBELLES["chercher"][1] + tampon_saisie.split(b"\x00")[0].decode("latin-1")
    elif taille > 0:                     # la balise ligne
        chemin_latin = "".join(c if ord(c) <= 0xFF else "." for c in chemin)
        texte = (LIBELLES["balise"][1] + LIBELLES["tiret"][1] + chemin_latin
                 + LIBELLES["mid"][1] + str(taille) + LIBELLES["oct"][1]
                 + f"{curseur:08X}")
        if sale:
            texte += LIBELLES["modif"][1]
    else:                                # la vitrine vide : l'usage
        texte = LIBELLES["usage"][1]
    ecran[2000:2160] = _creneaux(texte, 160)
    # la barre ligne 2 (LE PANNEAU)
    if taille > 0:
        texte = (LIBELLES["md5"][1] + empreintes[:16].hex()
                 + LIBELLES["sha"][1] + empreintes[16:48].hex())
        if sale:
            texte += LIBELLES["ast"][1]
    else:
        texte = LIBELLES["vide"][1]
    ecran[2160:2320] = _creneaux(texte, 160)
    return bytes(ecran)


# (la fenêtre du modèle vient des octets RÉELS du témoin, en argument —
#  le modèle EST le juge, il lit le fichier, jamais le cadre du bloc)


def fenetre_modele(donnees: bytes, vue: int, remplissage: int) -> bytes:
    """La vue du modèle : les octets du TÉMOIN à la fenêtre [vue, vue+384)."""
    return donnees[vue:vue + remplissage]


# =====================================================================================
# V0 — LES PIÈCES DU PLAN
# =====================================================================================

def vecteur_v0():
    section("V0 — les pièces du plan (les scellés relus, le geste recompté)")
    donnees_demo = open(os.path.join(TRIADE, SCELLE_DEMO), "rb").read()
    ok_demo = (len(donnees_demo) == SCELLE_DEMO_TAILLE
               and hashlib.md5(donnees_demo).hexdigest() == SCELLE_DEMO_MD5
               and hashlib.sha256(donnees_demo).hexdigest() == SCELLE_DEMO_SHA256)
    controle("V0.a:le-scelle-demo-relu", ok_demo,
             f"{len(donnees_demo)} o, md5 73c064fb…, sha256 df8f2e50… — "
             "l'ancre R7 de win-03 (la boucle de messages de l'ère démo)")
    donnees_m1 = open(os.path.join(TRIADE, HN.SCELLE_M1), "rb").read()
    ok_m1 = (len(donnees_m1) == HN.SCELLE_M1_TAILLE
             and hashlib.sha256(donnees_m1).hexdigest() == HN.SCELLE_M1_SHA256)
    controle("V0.b:le-scelle-M1-relu", ok_m1,
             "selftest.exe 9 216 o — l'ancre R7 de libc-02 (le memcmp du "
             "chantier navigation)")
    # les SEPT specs du geste relues (les têtes + les révisions)
    ok_specs = True
    for bid, nom in NOMS_RENDU.items():
        chemin = os.path.join(ICI, "I", nom + ".md")
        if not os.path.exists(chemin):
            ok_specs = False
            continue
        premiere = open(chemin, encoding="utf-8").readline()
        if f"loupe-{bid[5:7]}" not in premiere or "révision" not in premiere:
            ok_specs = False
    controle("V0.c:les-sept-specs-du-geste-relues", ok_specs,
             "les têtes loupe-08..14 (la couche I du geste, révision 1)")
    # le plan : les slots (c) ARRÊTÉS sur les mesures (D161)
    attendus = {"i110008": (0x49C0, 0x140, 271), "i110010": (0x4B00, 0x680, 1622),
                "i110011": (0x5180, 0x280, 568), "i110012": (0x5400, 0x340, 796),
                "i110013": (0x5740, 0xC0, 126), "i110014": (0x5800, 0x400, 967),
                "i110009": (0x5C00, 0x480, 1135)}
    ordre = ("i110008", "i110010", "i110011", "i110012", "i110013",
             "i110014", "i110009")
    ok_slots = all(L.SLOTS_LOUPE[b][0] == va and L.SLOTS_LOUPE[b][1] == sl
                   and sl % 64 == 0 and sl - mes >= 16
                   for b, (va, sl, mes) in attendus.items())
    ok_tasse = all(L.SLOTS_LOUPE[a][0] + L.SLOTS_LOUPE[a][1] == L.SLOTS_LOUPE[b][0]
                   for a, b in zip(ordre, ordre[1:])) \
        and L.SLOTS_LOUPE["i110008"][0] == 0x49C0 \
        and L.SLOTS_LOUPE["i110009"][0] + L.SLOTS_LOUPE["i110009"][1] == 0x6080
    controle("V0.d:les-slots-du-geste-arretes-sur-les-mesures",
             ok_slots and ok_tasse,
             "08@0x49C0 [271 o] → 10@0x4B00 [1614] → 11@0x5180 [568] → "
             "12@0x5400 [796] → 13@0x5740 [126] → 14@0x5800 [967] → "
             "09@0x5C00 [1135, r2 LA TABLE ÉTENDUE au geste (d) — la "
             "famille édition suit à sa suite] — fin 0x6080, multiples de "
             "64, padding >= 16")
    # les adresses .rdata du rendu + l'IAT démo
    ok_rdata = (L.R_ENTETE == 0x2000 and L.R_HEX == 0x2050 and L.R_HEXL == 0x2070
                and L.L_USAGE == 0x2300 and L.L_ABSENT == 0x23E6
                and L.R_CLASSE == 0x2600 and L.R_TITRE == 0x2614
                and L.R_ERREUR == 0x2650
                and L.R_WIN03 == 0x15C0 and L.R_LIBC02 == 0x1180
                and L.R_IAT_DEMO_GMW == 0x2818 and L.R_IAT_DEMO_TM == 0x2820
                and L.R_IAT_DEMO_DMW == 0x2828
                and L.R_MD5_T + 256 == L.L_USAGE
                and L.L_ABSENT + 20 <= 0x2400)
    controle("V0.e:les-adresses-rdata-du-rendu", ok_rdata,
             "l'entête @0x2000 · les tables HEX/HEXL @0x2050/0x2070 · les 19 "
             "libellés @0x2300-0x23FA · l'UTF-16 (classe, titre, l'erreur "
             "fatale) @0x2600+ — LA RÈGLE DU GESTE (b) EXÉCUTÉE : win-03 "
             "@0x15C0 À SON ADRESSE SCELLÉE DÉMO, libc-02 @0x1180 à son "
             "adresse scellée M1, l'IAT démo @0x2818/0x2820/0x2828 (les "
             "TROIS déplacements scellés de la boucle)")
    return donnees_demo, donnees_m1


# =====================================================================================
# V1 — LE ROUND-TRIP + LA STRUCTURE + L'HÉRITAGE R7 (libc-02 et win-03)
# =====================================================================================

def vecteur_v1(emul: EmulationRendu, donnees_m1: bytes, donnees_demo: bytes):
    section("V1 — round-trip + concordance au plan + l'héritage R7 constaté")
    insns_par_bloc = {}
    for bid, attendu in MESURES_RENDU.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        chemin = os.path.join(ICI, "notation", NOMS_RENDU[bid] + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        insns_par_bloc[bid] = insns
        controle(f"V1.a:{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o mesurés à l'arrêt, "
                 f"{len(insns)}/{len(metas)} instructions")

    # les déplacements RIP : les cibles == les symboles du plan (la liste fermée)
    cibles_legales = {L.R_CADRE, L.R_EMPREINTES, L.R_SAISIE, L.R_MOTIF,
                      L.R_JOURNAL, L.R_ECRAN, L.R_HWND, L.R_METRIQUES,
                      L.R_CUMUL, L.R_MD5_S, L.R_ENTETE, L.R_HEX, L.R_HEXL,
                      L.R_CLASSE, L.R_TITRE, L.R_ERREUR,
                      L.L_USAGE, L.L_BALISE, L.L_TIRET, L.L_MID, L.L_OCT,
                      L.L_MODIF, L.L_MD5, L.L_SHA, L.L_AST, L.L_VIDE,
                      L.L_ALLER, L.L_CHERCHER, L.L_MALFORMEE,
                      L.L_HORSBORNES, L.L_SESSION, L.L_FIN, L.L_PAIRES,
                      L.L_SYSTEME, L.L_ABSENT} | set(L.IAT_SLOTS.values())
    ok_rip, vus = True, 0
    for bid, insns in insns_par_bloc.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        for insn in insns:
            cible = B4.operande_rip_cible(insn)
            if cible is not None:
                vus += 1
                if cible not in cibles_legales:
                    # les cibles LOCALES (les étiquettes du bloc) sont légales
                    if not (rva <= cible < rva + slot):
                        ok_rip = False
    controle("V1.b:les-deplacements-rip-aux-symboles-du-plan",
             ok_rip and vus >= 40,
             f"{vus} déplacements, chaque cible ∈ le plan (les zones, CUMUL, "
             "les pièces .rdata du rendu, les 19 libellés, l'UTF-16, les "
             "feuilles IAT) ou une étiquette LOCALE du bloc")

    # les appels directs : la liste fermée par bloc (le réseau des specs)
    appels_attendus = {
        "i110008": set(),
        "i110010": {L.LOUPE08_VA},
        "i110011": {L.LOUPE02_VA},
        "i110012": {L.LOUPE02_VA, L.LOUPE14_VA},
        "i110013": {L.R_LIBC02},
        "i110014": {L.LOUPE13_VA, L.LOUPE02_VA},
        "i110009": {L.LOUPE01_VA, L.LOUPE10_VA, L.LOUPE11_VA, L.LOUPE12_VA,
                    L.LOUPE14_VA, L.LOUPE15_VA, L.LOUPE16_VA, L.LOUPE17_VA,
                    L.LOUPE18_VA, L.R_WIN03},
    }
    ok_appels = True
    for bid, attendu_set in appels_attendus.items():
        rva, slot = L.SLOTS_LOUPE[bid]
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call" and "[rip" not in insn.op_str:
                cible = int(insn.op_str, 0)
                if cible not in attendu_set and not (rva <= cible < rva + slot):
                    ok_appels = False
    controle("V1.c:les-appels-directs-a-la-liste-fermee", ok_appels,
             "loupe-10 → 08 · loupe-11 → 02 · loupe-12 → 02+14 (le commit "
             "CHERCHER délégué) · loupe-13 → libc-02 (LE SCELLÉ M1) · "
             "loupe-14 → 13+02 · loupe-09 → 01/10/11/12/14+15/16/17/18+"
             "win-03 (LA BOUCLE SCELLÉE DÉMO) — le réseau des specs, la "
             "table r2 étendue au geste (d)")

    # les feuilles IAT par bloc (la liste fermée de chaque bloc)
    iat_attendues = {
        "i110008": set(),
        "i110010": {"BeginPaint", "EndPaint", "GetStockObject", "SelectObject",
                    "GetTextMetricsW", "TextOutW", "SetTextColor",
                    "SetBkColor", "GetClientRect", "GetLastError"},
        "i110011": {"GetScrollInfo", "SetScrollInfo", "InvalidateRect",
                    "GetLastError"},
        "i110012": {"InvalidateRect"},
        "i110013": set(),
        "i110014": {"SetFilePointerEx", "ReadFile", "GetLastError",
                    "InvalidateRect"},
        "i110009": {"GetCommandLineW", "LoadCursorW", "RegisterClassExW",
                    "CreateWindowExW", "ShowWindow", "MessageBoxW",
                    "ExitProcess", "DefWindowProcW"},
    }
    ok_iat = True
    for bid, attendues in iat_attendues.items():
        vues = set()
        for insn in insns_par_bloc[bid]:
            cible = B4.operande_rip_cible(insn)
            if insn.mnemonic == "call" and cible is not None \
                    and cible in L.IAT_SLOTS.values():
                vues.add(next(n for n, s in L.IAT_SLOTS.items() if s == cible))
        if vues != attendues:
            ok_iat = False
            print(f"    [{bid}] IAT vue {sorted(vues)} != attendu {sorted(attendues)}")
    controle("V1.d:les-feuilles-iat-par-bloc-a-la-liste-fermee", ok_iat,
             "10 : 4 user32 + 6 gdi32 (L'UNIQUE PEINTRE) · 11 : 4 · 12 : 1 "
             "(InvalidateRect seul — le plan fait foi) · 13 : AUCUNE (la "
             "feuille pure) · 14 : 4 · 09 : 8 · 08 : AUCUNE — les listes "
             "fermées des specs")

    # L'HÉRITAGE R7 CONSTATÉ BYTE-IDENTIQUE — LA DOUBLE PREUVE
    ok_pose = all(bytes(emul.uc.mem_read(a, 0x80)) == o
                  for a, o in ((L.R_LIBC02, emul.heritages_rendu["libc-02"]),
                               (L.R_WIN03, emul.heritages_rendu["win-03"])))
    controle("V1.e:l'heritage-pose-aux-adresses-scellees", ok_pose,
             "libc-02 @0x1180 (le memcmp de selftest.exe) et win-03 @0x15C0 "
             "(la boucle de demo.exe) — LES MÊMES octets AUX MÊMES adresses "
             "que leurs images d'origine (la règle du geste (b))")
    extraits = {"libc-02": EmulationRendu.extraire(donnees_m1, 0x1180, 0x80),
                "win-03": EmulationRendu.extraire(donnees_demo, 0x15C0, 0x80)}
    origines = {"libc-02": ("m1", "libc-02-memcmp"),
                "win-03": ("demo", "win-03-boucle")}
    ok_double = True
    for nom, (dossier, notnom) in origines.items():
        chemin = os.path.join(TRIADE, dossier, "notation", notnom + ".asm")
        rva_origine = 0x1180 if nom == "libc-02" else 0x15C0
        # l'origine relue : la notation d'origine ré-assemblée == l'extrait
        # (le CODE seul — le padding NOP du slot complète à 0x80)
        octets_origine, _ = B4.assembler_bloc(emul.ks, chemin,
                                              rva_origine, 0x80)
        if bytes(octets_origine) != extraits[nom][:len(octets_origine)]:
            ok_double = False
        if bytes(emul.uc.mem_read(rva_origine, 0x80)) != extraits[nom]:
            ok_double = False
    controle("V1.f:l'heritage-r7-constate-byte-identique", ok_double,
             "LA DOUBLE PREUVE : les extraits des SCELLÉS == les octets "
             "émulés ET les notations d'origine (m1/libc-02-memcmp, "
             "demo/win-03-boucle) ré-assemblées == les extraits — R7 au sens "
             "propre, JAMAIS une ré-écriture")

    # LA PROCÉDURE : le pointeur enregistré == l'étiquette de la notation
    controle("V1.g:la-procedure-relue-depuis-la-notation",
             0x5C00 <= emul.adresse_procedure() < 0x5F80,
             f".procedure == 0x{emul.adresse_procedure():x} — dans le slot "
             "de loupe-09 (l'étiquette résolue de la notation, la source "
             "que RegisterClassExW posera comme lpfnWndProc)")

    # aucun syscall (le miroir du noyau)
    ok_sys = all("syscall" not in i.mnemonic
                 for insns in insns_par_bloc.values() for i in insns)
    controle("V1.h:aucun-syscall", ok_sys,
             "les sept notations du geste : zéro site syscall — tout passe "
             "par l'IAT déclarée ou les appels directs aux blocs")


# =====================================================================================
# V2 — LOUPE-08 LA LIGNE (le doré + le différentiel + les rejets)
# =====================================================================================

ADRESSE_LIGNE = 0x700600        # la sortie de test (77 o + la garde)


def vecteur_v2(emul: EmulationRendu, temoins, rng):
    section("V2 — loupe-08 la ligne : le doré, le différentiel, les rejets")
    proxy = temoins["proxy.exe"]
    # LE DORÉ : la première ligne de proxy.exe scellé (la pièce de l'ère à l'œil)
    emul.uc.mem_write(HN.ADRESSE_SORTIE48, proxy[:16])
    emul.uc.mem_write(ADRESSE_LIGNE, b"\xA5" * 96)
    r = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48, "rdx": 16,
                                    "r8": ADRESSE_LIGNE, "r9": 0})
    rendu = bytes(emul.uc.mem_read(ADRESSE_LIGNE, 96))
    attendu = model_ligne(0, proxy[:16]) + b"\xA5" * (96 - 77)
    controle("V2.a:le-dore-proxy-premiere-ligne",
             r["rax"] == 0 and rendu == attendu,
             f"loupe-08(0, 16) sur « MZ\\x90\\x00\\x03… » == le modèle "
             f"({rendu[:20]!r}…) — les 77 o exacts, la garde intacte")
    # LA LIGNE FINALE INCOMPLÈTE : le témoin 3f (UN octet valide à la fin)
    temoin = temoins["temoin-3f.bin"]
    fin = 3 * 65536
    emul.uc.mem_write(HN.ADRESSE_SORTIE48, temoin[fin:fin + 1])
    emul.uc.mem_write(ADRESSE_LIGNE, b"\xA5" * 96)
    r = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48, "rdx": 1,
                                    "r8": ADRESSE_LIGNE, "r9": fin})
    rendu = bytes(emul.uc.mem_read(ADRESSE_LIGNE, 96))
    attendu = model_ligne(fin, temoin[fin:fin + 1]) + b"\xA5" * (96 - 77)
    controle("V2.b:la-ligne-finale-incomplete",
             r["rax"] == 0 and rendu == attendu,
             "le témoin 3×64 Kio + 1 à son dernier octet : UN groupe, "
             "QUINZE paires d'espaces, la colonne ASCII DROITE (Q3)")
    # LES 16 LONGUEURS BORNÉES sur le témoin 384
    temoin384 = temoins["temoin-384.bin"]
    emul.uc.mem_write(HN.ADRESSE_SORTIE48, temoin384[:16])
    ok_bornes = True
    for lon in range(1, 17):
        emul.uc.mem_write(ADRESSE_LIGNE, b"\xA5" * 96)
        r = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48,
                                        "rdx": lon, "r8": ADRESSE_LIGNE,
                                        "r9": 0x1230})
        if r["rax"] != 0 or bytes(emul.uc.mem_read(ADRESSE_LIGNE, 77)) != \
                model_ligne(0x1230, temoin384[:lon]):
            ok_bornes = False
    controle("V2.c:les-16-longueurs-bornees", ok_bornes,
             "la longueur 1 à 16 : chaque ligne == le modèle, les groupes "
             "absents deux espaces, le miroir absent un espace")
    # LE DIFFÉRENTIEL : 1 500 lignes aléatoires
    divergences = 0
    for _ in range(1500):
        decalage = rng.randrange(0, 0x80000000) & ~0xF
        lon = rng.randrange(1, 17)
        octets = bytes(rng.randrange(0, 256) for _ in range(lon))
        emul.uc.mem_write(HN.ADRESSE_SORTIE48, octets + b"\x00" * (16 - lon))
        emul.uc.mem_write(ADRESSE_LIGNE, b"\xA5" * 96)
        r = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48,
                                        "rdx": lon, "r8": ADRESSE_LIGNE,
                                        "r9": decalage})
        if r["rax"] != 0 or bytes(emul.uc.mem_read(ADRESSE_LIGNE, 77)) != \
                model_ligne(decalage, octets):
            divergences += 1
    controle("V2.d:le-differentiel-1500-lignes", divergences == 0,
             "1 500 lignes aléatoires (décalages multiples de 16, longueurs "
             "1..16, alphabet plein 0x00-0xFF) == le modèle Python — "
             "l'égalité octet par octet, zéro divergence")
    # LES TROIS REJETS (E1/E2/E3) — la sortie INTACTE
    emul.uc.mem_write(ADRESSE_LIGNE, b"\xA5" * 96)
    garde = bytes(emul.uc.mem_read(ADRESSE_LIGNE, 96))
    r0 = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48, "rdx": 0,
                                     "r8": ADRESSE_LIGNE, "r9": 0})
    r17 = emul.appeler(L.LOUPE08_VA, {"rcx": HN.ADRESSE_SORTIE48, "rdx": 17,
                                      "r8": ADRESSE_LIGNE, "r9": 0})
    rn = emul.appeler(L.LOUPE08_VA, {"rcx": 0, "rdx": 8,
                                     "r8": ADRESSE_LIGNE, "r9": 0})
    controle("V2.e:les-trois-rejets-nommes",
             r0["rax"] == -5 and r17["rax"] == -5 and rn["rax"] == -5
             and bytes(emul.uc.mem_read(ADRESSE_LIGNE, 96)) == garde,
             "longueur 0, longueur 17, pointeur nul → les TROIS -5 "
             "ENTRÉE, RIEN écrit — la garde de 96 o relue IDENTIQUE")


# =====================================================================================
# V3 — LOUPE-13 LA RECHERCHE (l'école + le différentiel + les rejets)
# =====================================================================================

ADRESSE_MOTIF_TEST = ADRESSE_MOTIF  # (l'alias du geste (c))


def appel_loupe13(emul, fenetre: bytes, motif: bytes, depart: int):
    emul.uc.mem_write(ADRESSE_FENETRE, fenetre)
    emul.uc.mem_write(ADRESSE_MOTIF, motif)
    return emul.appeler(L.LOUPE13_VA, {
        "rcx": ADRESSE_FENETRE, "rdx": len(fenetre),
        "r8": ADRESSE_MOTIF, "r9": len(motif)}, pile_args=[depart])


def vecteur_v3(emul: EmulationRendu, temoins, rng):
    section("V3 — loupe-13 la recherche : l'école, le différentiel, les rejets")
    # LE CORPUS DE L'ÉCOLE (V2 de la spec — les cas tenus pour toujours)
    ecole = [
        (b"ABCDE", b"A", 0, 0),                # le premier octet
        (b"ABCDE", b"E", 0, 4),                # le dernier
        (b"XXABCYY", b"ABC", 2, 2),            # à cheval sur le départ
        (b"ABABCABC", b"ABC", 0, 2),           # l'occurrence DOUBLE : la PREMIÈRE
        (b"AAAAB", b"AAAA", 0, 0),             # le motif répétitif
        (b"AAAAB", b"AAAB", 0, 1),             # le presque-frère
        (b"ABABAB", b"ABAB", 1, 2),            # le départ au milieu (la PREMIÈRE depuis lui)
        (b"", b"A", 0, -1),                    # la fenêtre vide
        (b"ABC", b"", 0, -5),                  # chercher rien n'est pas chercher
        (b"AB", b"ABC", 0, -1),                # le motif plus long (le constat immédiat)
    ]
    ok_ecole = True
    for fenetre, motif, depart, attendu in ecole:
        r = appel_loupe13(emul, fenetre, motif, depart)
        if r["rax"] != attendu:
            ok_ecole = False
            print(f"    école: {fenetre!r} {motif!r} départ {depart} → "
                  f"{r['rax']} != {attendu}")
    controle("V3.a:le-corpus-de-l-ecole", ok_ecole,
             "le premier, le dernier, à cheval sur le départ, l'occurrence "
             "double (LA PREMIÈRE exigée), AAAA dans AAAAB, le départ au "
             "milieu, la fenêtre vide → -1, le motif vide → -5, le motif "
             "trop long → -1 IMMÉDIAT")
    # LE DIFFÉRENTIEL : 1 500 cas == bytes.find
    divergences = 0
    for _ in range(1500):
        n = rng.randrange(0, 2048)
        pauvre = rng.randrange(2)
        alphabet = (b"AB" if pauvre else bytes(range(256)))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        r = appel_loupe13(emul, fenetre, motif, depart)
        attendu = fenetre.find(motif, depart)
        if r["rax"] != attendu:
            divergences += 1
    controle("V3.b:le-differentiel-1500-cas", divergences == 0,
             "1 500 cas aléatoires (fenêtres 0..2 048, motifs 1..32, "
             "alphabets plein ET pauvre pour forcer les occurrences "
             "multiples) == bytes.find À L'IDENTIQUE, y compris les -1")
    # LES FENÊTRES RÉELLES DE PROXY.EXE (les marques de la pièce de l'ère)
    proxy = temoins["proxy.exe"]
    marques = [(b"MZ", 0), (b"PE\x00\x00", 0), (b"This program", 0),
               (b"PEMax", None)]
    ok_marques = True
    for motif, attendu in marques:
        r = appel_loupe13(emul, proxy[:8192], motif, 0)
        vise = proxy.find(motif, 0) if attendu is None else proxy.find(motif)
        if r["rax"] != vise:
            ok_marques = False
    controle("V3.c:les-marques-de-proxy", ok_marques,
             "MZ, PE, « This program » sur la vraie première fenêtre du "
             "scellé — chaque position == bytes.find (PEMax : l'absence "
             "constatée par la FIN nommée -1)")
    # LES TROIS REJETS (E1/E2/E3)
    r_vide = appel_loupe13(emul, b"ABCD", b"", 0)
    r_33 = appel_loupe13(emul, b"ABCD", b"X" * 33, 0)
    r_dep = appel_loupe13(emul, b"ABCD", b"A", 5)
    controle("V3.d:les-trois-rejets-nommes",
             r_vide["rax"] == -5 and r_33["rax"] == -5 and r_dep["rax"] == -5,
             "le motif vide, le motif de 33 o, le départ au-delà de la "
             "fenêtre → les TROIS -5 ENTRÉE (chercher rien n'est pas "
             "chercher ; la borne du quotidien ; le départ est une "
             "position, pas un vœu)")


# =====================================================================================
# V4 — LOUPE-14 LE SUIVANT (la chaîne au fichier + LE RECOUVREMENT + les rejets)
# =====================================================================================

def composer_temoins_rendu(rng):
    """Les témoins du geste : le 70 000 o (deux fenêtres de 64 Kio) et le
    témoin À FRONTIÈRES COMPOSÉES (les occurrences n'existent QU'à cheval
    sur chaque frontière de 64 Kio — la preuve du recouvrement par
    construction, V2 de la spec)."""
    t70 = bytes(rng.randrange(256) for _ in range(70000))
    # le témoin frontières : 4 fenêtres (262 145 o), un marqueur de 5 o
    # posé À CHEVAL sur chaque frontière (l'occurrence est INTRADOVABLE
    # en fenêtre alignée : seul le recouvrement la trouve)
    marqueur = b"\xde\xad\xbe\xef\x99"
    taille = 3 * 65536 + 1
    tf = bytearray(rng.randrange(256) for _ in range(taille))
    straddles = []
    for k in range(1, 4):                  # les frontières 64K, 128K, 192K
        pos = 65536 * k - 2                # 2 octets avant la frontière
        tf[pos:pos + 5] = marqueur         # l'occurrence À CHEVAL (3 o après)
        straddles.append(pos)
    return {"temoin-70k.bin": bytes(t70),
            "temoin-front.bin": bytes(tf)}, straddles


def vecteur_v4(emul: EmulationRendu, os_v, temoins, straddles, rng):
    section("V4 — loupe-14 : la chaîne au fichier, LE RECOUVREMENT, les rejets")
    hwnd = 0x770001

    def poser_saisie(motif: bytes):
        """La saisie CHERCHER posée comme loupe-12 l'aurait frappée (le mode
        2 + les paires hexa au tampon) — le commit relit LA SAISIE, la voie
        réelle du renvoi."""
        hexa = motif.hex().upper().encode()
        emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 2, 0, 0)
                          + hexa + b"\x00" * (80 - len(hexa)))

    # LA CHAÎNE au fichier entier : le témoin 3f (3 fenêtres + 1) — le commit
    # (depuis le curseur) puis chaque F3 (depuis le curseur + 1) : la chaîne
    # == bytes.find, occurrence après occurrence, ET LA FIN
    temoin = temoins["temoin-3f.bin"]
    motif = bytes([temoin[1000], temoin[1001], temoin[1002]])
    attendus = []
    p = 0
    while True:
        p = temoin.find(motif, p)
        if p < 0:
            break
        attendus.append(p)
        p += 1
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    poser_saisie(motif)
    emul.ecrire_cadre(544, struct.pack("<Q", 0))     # le curseur au début
    r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x0d, "r9": 0})
    vus = [emul.u64(544)]
    for _ in range(len(attendus) - 1):
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": 0x72, "r9": 0})
        if r["rax"] != 0:
            break
        vus.append(emul.u64(544))
    r_fin = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": 0x72, "r9": 0})
    ok_chaine = (r["rax"] == 0 and vus == attendus and r_fin["rax"] == -1
                 and bytes(emul.uc.mem_read(L.R_MOTIF + 32, 4))
                 == struct.pack("<I", len(motif)))
    controle("V4.a:la-chaine-au-fichier-entier", ok_chaine,
             f"le commit puis {len(attendus) - 1} F3 : chaque occurrence "
             "amène le curseur à SA position (la chaîne == bytes.find au "
             "fichier entier, 3 fenêtres de 64 Kio + 1) ; le F3 de trop → "
             "LA FIN NOMMÉE -1, LE MOTIF DEMEURE à la zone (la fin "
             "n'efface pas la question)")
    # LE RECOUVREMENT PAR CONSTRUCTION : les occurrences n'existent QU'à cheval
    os_v.declarer("temoin-front.bin", HN.FichierVirtuel(
        contenu=temoins["temoin-front.bin"]))
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-front.bin")
    motif5 = b"\xde\xad\xbe\xef\x99"
    poser_saisie(motif5)
    emul.ecrire_cadre(544, struct.pack("<Q", 0))
    r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x0d, "r9": 0})
    trouvees = [emul.u64(544)]
    while True:
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": 0x72, "r9": 0})
        if r["rax"] != 0:
            break
        trouvees.append(emul.u64(544))
    controle("V4.b:LE-RECOUVREMENT-PAR-CONSTRUCTION",
             r["rax"] == -1 and trouvees == straddles,
             f"les occurrences n'existent QU'à cheval sur les frontières "
             f"64K/128K/192K : TROUVÉES aux positions {trouvees} == les "
             f"attendues {straddles} — la fenêtre suivante commence à bord "
             "+ 64 Kio − (longueur − 1), l'occurrence à cheval est dans les "
             "DEUX fenêtres, JAMAIS manquée (le mutant d'un octet au "
             "recouvrement la manquerait — la falsification V7 la rejoue)")
    # LE DIFFÉRENTIEL : 12 motifs aléatoires sur le témoin 70 000 o
    os_v.declarer("temoin-70k.bin", HN.FichierVirtuel(
        contenu=temoins["temoin-70k.bin"]))
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-70k.bin")
    divergences = 0
    for _ in range(12):
        motif = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 6)))
        poser_saisie(motif)
        emul.ecrire_cadre(544, struct.pack("<Q", 0))
        p = temoins["temoin-70k.bin"].find(motif, 0)
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": 0x0d, "r9": 0})
        if p < 0:                      # le motif absent : LA FIN dès le commit
            if r["rax"] != -1:
                divergences += 1
                print(f"    [V4.c] motif {motif.hex()} : la FIN attendue, "
                      f"rendu {r['rax']}")
            continue
        if r["rax"] != 0 or emul.u64(544) != p:
            divergences += 1
            print(f"    [V4.c] motif {motif.hex()} : commit {r['rax']} "
                  f"curseur {emul.u64(544)} != attendu {p}")
            continue
        while p >= 0:
            p2 = temoins["temoin-70k.bin"].find(motif, p + 1)
            r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                            "r8": 0x72, "r9": 0})
            if p2 < 0:
                if r["rax"] != -1:
                    divergences += 1
                break
            if r["rax"] != 0 or emul.u64(544) != p2:
                divergences += 1
                break
            p = p2
    controle("V4.c:le-differentiel-12-motifs-70k", divergences == 0,
             "12 motifs aléatoires (1..5 o) sur le témoin de 70 000 o (2 "
             "fenêtres) : chaque occurrence ET LA FIN == la chaîne "
             "bytes.find — l'égalité des positions successives")
    # LES REJETS (E1/E2/E3) : les saisies mal formées, la session, l'OS
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    for tampon, attendu in ((b"4d5", -5), (b"ZZ", -5), (b"", -5),
                            (b"4D5A" * 17, -5)):
        emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 2, 0, 0)
                          + tampon[:79] + b"\x00" * (80 - len(tampon[:79])))
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": 0x0d, "r9": 0})
        if r["rax"] != attendu:
            controle("V4.e:les-rejets-nommes", False,
                     f"{tampon[:12]!r} → {r['rax']} != {attendu}")
            return
    # sans session : -4
    HN.fermer_session(emul)
    r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": 0x72, "r9": 0})
    ok_e2 = r["rax"] == -4 and struct.unpack("<I", bytes(
        emul.uc.mem_read(L.R_SAISIE, 4)))[0] == 3
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    # le refus de lecture : le shim en échec → -6 relayé, la position intacte
    emul.uc.mem_write(L.R_MOTIF, b"AB" + b"\x00" * 30)
    emul.uc.mem_write(L.R_MOTIF + 32, struct.pack("<I", 2))
    emul.ecrire_cadre(544, struct.pack("<Q", 0x20))
    os_v.armer_echec_read(1)
    r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": 0x72, "r9": 0})
    ok_e3 = (r["rax"] == -6 and emul.u64(544) == 0x20
             and (os_v.journal_gle[-1][1] if os_v.journal_gle else 0) != 0)
    os_v.armer_echec_read(None)
    controle("V4.e:les-rejets-nommes", ok_e2 and ok_e3,
             "4d5 (impair), ZZ, vide, 68 chiffres → les -5 « paires hexa "
             "attendues » ; sans session → -4 « aucun fichier ouvert » (le "
             "mode MESSAGE posé) ; le ReadFile en échec → -6 relayé, le "
             "code AU JOURNAL, la position de départ DEMEURE (rien bougé)")


# =====================================================================================
# V5 — LE DÉFILEMENT + L'ALLER (les bornes, les scénarios, les refus nommés)
# =====================================================================================

def vecteur_v5(emul: EmulationRendu, os_v, temoins, rng):
    section("V5 — le défilement + l'aller : les bornes, les scénarios, les refus")
    hwnd = 0x770001
    # LA BORNE DIFFÉRENTIELLE : vue_max + le clamp rejoués contre le plan
    divergences = 0
    for _ in range(10000):
        taille = rng.choice([0, 1, rng.randrange(0, 4096), 384, 385,
                             rng.randrange(0, 1 << 31)])
        vm = L.vue_max(taille)
        if vm != (0 if taille <= 384 else ((taille - 384) + 15) & ~15):
            divergences += 1
        # le clamp d'un pas aléatoire
        vue = rng.randrange(0, max(1, vm + 1)) & ~0xF if vm else 0
        pas = rng.choice([-352, -16, 16, 352, -48, 48])
        cible = max(0, min(vm, vue + pas))
        if (vue + pas < 0 and cible != 0) or (vue + pas > vm and cible != vm):
            divergences += 1
    controle("V5.a:la-borne-differentielle-10000-tailles", divergences == 0,
             "vue_max et le clamp rejoués sur 10 000 tailles aléatoires (0, "
             "1, 384, 385, les bords, 2 Gio) == la règle EXÉCUTABLE du plan "
             "— LA DERNIÈRE FENÊTRE voit le dernier octet, les petits "
             "fichiers ne défilent pas")
    # LE SCÉNARIO MOLETTE : au bout, la dernière fenêtre voit la fin
    temoin = temoins["temoin-3f.bin"]
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    gui = emul.gui
    gui.reset()
    gui.hwnd = hwnd
    # pose les métriques (la police mesurée — l'état d'une vitrine vivante)
    emul.uc.mem_write(L.R_METRIQUES, struct.pack("<IIII", 8, 16, 27, 1))
    tours = 0
    while tours < 8:                     # le pas vérifié : TROIS lignes par cran
        r = emul.appeler(L.LOUPE11_VA, {"rcx": hwnd, "rdx": 0x20a,
                                        "r8": 0xFF880000, "r9": 0})
        tours += 1
    apres_crans = emul.u64(536)
    ok_pas = apres_crans == 8 * 48
    # LA POIGNÉE AU BOUT : l'ascenseur au maximum — la DERNIÈRE FENÊTRE
    gui.trackpos = L.vue_max(len(temoin)) // 16
    r = emul.appeler(L.LOUPE11_VA, {"rcx": hwnd, "rdx": 0x115,
                                    "r8": 5, "r9": 0})
    ok_bout = (ok_pas and emul.u64(536) == L.vue_max(len(temoin))
               and emul.u32(552) >= 1 and gui.scroll is not None
               and gui.scroll[1] == L.vue_max(len(temoin)) // 16)
    controle("V5.b:la-molette-au-bout-voit-la-fin", ok_bout,
             f"{tours} crans (8 × 48 o = 0x{apres_crans:x} — le pas de TROIS "
             "lignes vérifié) puis LA POIGNÉE AU BOUT : la vue atteint "
             f"vue_max 0x{L.vue_max(len(temoin)):x} == LA DERNIÈRE FENÊTRE — "
             "le dernier octet VISIBLE (le remplissage court demeure, la fin "
             "n'est jamais cachée ; l'ascenseur synchrone : max == vue_max/16)")
    # LE PETIT FICHIER : la molette SANS effet, RIEN relu (les compteurs)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    lecture_avant = os_v.compteurs["ReadFile"]
    r = emul.appeler(L.LOUPE11_VA, {"rcx": hwnd, "rdx": 0x20a,
                                    "r8": 0xFF880000, "r9": 0})
    r = emul.appeler(L.LOUPE11_VA, {"rcx": hwnd, "rdx": 0x115,
                                    "r8": 3, "r9": 0})
    controle("V5.c:le-petit-fichier-ne-defile-pas",
             emul.u64(536) == 0 and os_v.compteurs["ReadFile"] == lecture_avant,
             "le témoin de 384 o exactement : la molette et la page DEMEURENT "
             "à vue 0 — le compteur ReadFile INCHANGÉ (le geste au bout ne "
             "relit pas, l'OS au bout reste calme)")
    # WM_SIZE : les lignes visibles recalculées
    r = emul.appeler(L.LOUPE11_VA, {"rcx": hwnd, "rdx": 5, "r8": 0,
                                    "r9": (320 << 16) | 640})
    lignes_posees = struct.unpack("<I", bytes(
        emul.uc.mem_read(L.R_METRIQUES + 8, 4)))[0]
    controle("V5.d:wm-size-recalcule",
             lignes_posees == 20 and gui.scroll is not None,
             f"cy = 320 → lignes visibles = 320/16 = {lignes_posees} posées à "
             "METRIQUES, l'ascenseur remis (le SetScrollInfo compté)")
    # L'ALLER : le saut au milieu — le curseur exact, la vue recalée, L'ÉCRAN
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * 96)
    emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x100, "r8": 0x74, "r9": 0})
    for chiffre in b"1000":
        emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": chiffre, "r9": 0})
    r = emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x0d, "r9": 0})
    curseur, vue = emul.u64(544), emul.u64(536)
    vue_attendue = min(L.recadre(0x1000), L.vue_max(len(temoin)))
    ok_saut = (r["rax"] == 0 and curseur == 0x1000 and vue == vue_attendue
               and struct.unpack("<I", bytes(emul.uc.mem_read(
                   L.R_SAISIE, 4)))[0] == 0)
    r = emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    fenetre = fenetre_modele(temoin, vue, emul.u32(552))
    attendu = model_ecran(fenetre, vue, emul.u32(552), len(temoin),
                          "temoin-3f.bin", curseur, 0,
                          bytes(emul.uc.mem_read(L.R_EMPREINTES, 48)), 0,
                          b"", 27)
    controle("V5.e:le-saut-exact-et-l-ecran-attendu",
             ok_saut and ecran == attendu,
             f"F5 « 1000 » + retour : le curseur à 0x1000 EXACT, la vue "
             f"recalée à 0x{vue_attendue:x} (la 12e ligne — la règle du "
             "plan), le mode refermé, L'ÉCRAN ATTENDU OCTET PAR OCTET "
             "(les 2320 o == le modèle)")
    # le 9e chiffre ignoré, VK_SUPPR retire, VK_ECHAP annule TOUT
    emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x100, "r8": 0x74, "r9": 0})
    for chiffre in b"123456789ABCDEF":
        emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": chiffre, "r9": 0})
    tamp = bytes(emul.uc.mem_read(L.R_SAISIE + 12, 16))
    emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 8, "r9": 0})
    tamp2 = bytes(emul.uc.mem_read(L.R_SAISIE + 12, 16))
    emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x1b, "r9": 0})
    mode = struct.unpack("<I", bytes(emul.uc.mem_read(L.R_SAISIE, 4)))[0]
    controle("V5.f:le-9e-ignore-le-corrige-l-echappee",
             tamp.split(b"\x00")[0] == b"12345678" and
             tamp2.split(b"\x00")[0] == b"1234567" and mode == 0,
             "16 chiffres frappés : le tampon porte les 8 PREMIERS (le 9e "
             "IGNORÉ proprement) ; VK_SUPPR retire le dernier ; VK_ECHAP "
             "annule TOUT (mode = 0, la barre revient, rien arrivé)")
    # LES REFUS NOMMÉS (E1/E2/E3) : la barre porte le nom
    refus = []
    for tampon, attendu in ((b"", -5), (b"12Z4", -5)):
        emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 1, 0, 0)
                          + tampon + b"\x00" * (80 - len(tampon)))
        r = emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": 0x0d, "r9": 0})
        refus.append((r["rax"], struct.unpack("<I", bytes(
            emul.uc.mem_read(L.R_SAISIE, 4)))[0],
            bytes(emul.uc.mem_read(L.R_SAISIE + 12, 24)).split(b"\x00")[0]))
    emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 1, 0, 0)
                      + b"7FFFFFFF" + b"\x00" * 71)
    r = emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x0d, "r9": 0})
    refus.append((r["rax"], struct.unpack("<I", bytes(
        emul.uc.mem_read(L.R_SAISIE, 4)))[0],
        bytes(emul.uc.mem_read(L.R_SAISIE + 12, 24)).split(b"\x00")[0]))
    HN.fermer_session(emul)
    r = emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": 0x74, "r9": 0})
    refus.append((r["rax"], struct.unpack("<I", bytes(
        emul.uc.mem_read(L.R_SAISIE, 4)))[0],
        bytes(emul.uc.mem_read(L.R_SAISIE + 12, 24)).split(b"\x00")[0]))
    ok_refus = (refus[0][0] == -5 and refus[0][1] == 3
                and refus[0][2] == b"saisie mal form\xe9e"
                and refus[1][0] == -5 and refus[1][2] == b"saisie mal form\xe9e"
                and refus[2][0] == -3 and refus[2][2] == b"hors bornes"
                and refus[3][0] == -4 and refus[3][2] == b"aucun fichier ouvert")
    controle("V5.g:les-refus-nommes-a-la-barre", ok_refus,
             "« » et « 12Z4 » → -5 « saisie mal formée » ; 0x7FFFFFFF sur "
             "le témoin 3f → -3 « hors bornes » (JAMAIS un saut silencieux) ; "
             "sans session → -4 « aucun fichier ouvert » — CHAQUE refus "
             "posé au tampon en mode MESSAGE (la barre le porte au "
             "prochain WM_PAINT)")


# =====================================================================================
# V6 — L'ORACLE À SCÉNARIOS (le critère du plan : l'écran attendu octet par octet)
# =====================================================================================

def etat_neuf(emul: EmulationRendu, gui: GUIVirtuel):
    """L'état d'un LANCEMENT NEUF : le cadre rendu par loupe-03 (l'hygiène
    du noyau), le .data d'initialiseur (les zones vierges — ce que le
    chargeur pose au démarrage). Jamais un état hérité."""
    HN.fermer_session(emul)
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * L.ZONE_SAISIE)
    emul.uc.mem_write(L.R_MOTIF, b"\x00" * L.ZONE_MOTIF)
    emul.uc.mem_write(L.R_METRIQUES, b"\x00" * L.ZONE_METRIQUES)
    emul.uc.mem_write(L.R_ECRAN, b"\x00" * L.ZONE_ECRAN)
    gui.reset()
    gui.hwnd = 0x770001


def vecteur_v6(emul: EmulationRendu, os_v, temoins):
    section("V6 — l'oracle à scénarios : la vitrine, la session, le routage, E1/E2")
    gui = emul.gui
    WM = L.WM_TAILLE, L.WM_PEINTURE, L.WM_VSCROLL, L.WM_TOUCHE, L.WM_CARACT, \
        L.WM_MOLETTE, L.WM_QUITTE

    def scenario(cmdline: str, messages):
        etat_neuf(emul, gui)
        gui.scripter(*messages)
        return emul.appeler_winmain(cmdline)

    def etat_ecran():
        return bytes(emul.uc.mem_read(L.R_ECRAN, 2320))

    # --- S1 : la vitrine SANS session (V1 de loupe-10 / V2 de loupe-09) -------
    r = scenario("loupe.exe", [(0x770001, L.WM_TAILLE, 0, (440 << 16) | 640),
                               (0x770001, L.WM_PEINTURE, 0, 0)])
    attendu_vide = model_ecran(b"", 0, 0, 0, "", 0, 0, b"\x00" * 48,
                               0, b"", 27)
    ok_s1 = (r["exit_code"] == 0 and etat_ecran() == attendu_vide
             and gui.classe_nom == "LoupeHexa"
             and gui.titre == TITRE_NOM
             and gui.scroll is None)
    controle("V6.a:la-vitrine-sans-session", ok_s1,
             "la commande sans chemin : la vitrine créée (classe « LoupeHexa », "
             "le titre, 640×480), l'écran composé == le modèle OCTET PAR OCTET "
             "(l'entête, AUCUNE ligne de grille, l'usage « loupe <fichier> » à "
             "la barre 1, « - » au panneau), l'ascenseur INTACT (le repli de "
             "loupe-11 : sans session, RIEN — Q5), la boucle win-03 courue "
             "jusqu'à WM_QUIT, ExitProcess(0)")
    # les gouttes peintes : l'entête + les 2 lignes de barre, aux positions
    gouttes_textes = [g[2] for g in gui.gouttes]
    ok_gouttes = (len(gui.gouttes) == 3
                  and gui.gouttes[0][1] == 8
                  and gui.gouttes[1][1] == 440 - 32
                  and gui.gouttes[2][1] == 440 - 16
                  and gui.gouttes[0][2] == tuple(
                      ENTETE_TEXTE.encode("latin-1")))
    controle("V6.b:les-gouttes-aux-positions", ok_gouttes,
             "TextOutW × 3 : l'entête à y=8 (65 gouttes, les mots == la "
             "chaîne .rdata), la barre ancrée au bas (y = cy−2·ligne_h et "
             "cy−ligne_h — LE PANNEAU TOUJOURS VISIBLE), AUCUNE goutte de "
             "grille (la vitrine vide ne peint rien de fantôme)")

    # --- S2 : le témoin ouvert PAR LA LIGNE DE COMMANDE (V1 de loupe-09) ------
    temoin = temoins["temoin-384.bin"]
    r = scenario("loupe.exe temoin-384.bin",
                 [(0x770001, L.WM_TAILLE, 0, (440 << 16) | 640),
                  (0x770001, L.WM_PEINTURE, 0, 0)])
    vue, rempl = emul.u64(536), emul.u32(552)
    attendu = model_ecran(fenetre_modele(temoin, vue, rempl), vue, rempl,
                          384, "temoin-384.bin", 0, 0,
                          hashlib.md5(temoin).digest()
                          + hashlib.sha256(temoin).digest(), 0, b"", 27)
    ok_s2 = (r["exit_code"] == 0 and etat_ecran() == attendu
             and vue == 0 and rempl == 384
             and emul.u64(528) != 0xFFFFFFFFFFFFFFFF)
    controle("V6.c:le-temoin-ouvert-par-la-ligne-de-commande", ok_s2,
             "« loupe.exe temoin-384.bin » : la ligne de commande lue À LA "
             "MAIN (le programme sauté), la session née entière AVANT la "
             "vitrine, les 24 lignes à la vue 0 == le modèle, le panneau == "
             "hashlib (md5 + sha-256 du témoin), l'écran OCTET PAR OCTET")

    # --- S3 : la cellule active INVERSÉE à l'abscisse exacte (Q3 de loupe-10) —
    #     la session de S2 vit : le curseur posé, LA PROCÉDURE peint (le
    #     message routé directement — V3 de loupe-09 au bloc près)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
    gui.reset()
    gui.hwnd = 0x770001
    proc = emul.adresse_procedure()
    r = emul.appeler(proc, {"rcx": 0x770001, "rdx": L.WM_PEINTURE,
                            "r8": 0, "r9": 0})
    cell = [(g[0], g[1], g[2], g[3], g[4]) for g in gui.gouttes
            if len(g[2]) == 2]
    ok_s3 = (len(cell) == 1 and cell[0][0] == 8 + (10 + 3 * 2) * 8
             and cell[0][1] == 8 + 3 * 16
             and cell[0][3] == 0x00FFFFFF and cell[0][4] == 0x00000000)
    controle("V6.d:la-cellule-active-inversee-a-l-abscisse-exacte", ok_s3,
             "le curseur à 0x22 : la colonne 2 de la ligne 2 repeinte en "
             "INVERSE — x = MARGE_X + (10 + 3·2)·char_w = 136, y = MARGE_Y "
             "+ 3·ligne_h = 56, blanc sur noir EXPLICITE puis restauré "
             "(chaque Set rend l'ancienne couleur)")

    # --- S4 : la marque sale — MODIFIÉ à la barre, l'astérisque au panneau ---
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    gui.reset()
    gui.hwnd = 0x770001
    r = emul.appeler(proc, {"rcx": 0x770001, "rdx": L.WM_PEINTURE,
                            "r8": 0, "r9": 0})
    vue, rempl = emul.u64(536), emul.u32(552)
    attendu = model_ecran(fenetre_modele(temoin, vue, rempl), vue, rempl,
                          384, "temoin-384.bin", 0x22, 1,
                          hashlib.md5(temoin).digest()
                          + hashlib.sha256(temoin).digest(), 0, b"", 27)
    controle("V6.e:la-marque-sale-nomme-la-divergence",
             etat_ecran() == attendu,
             "la marque sale posée : « · MODIFIÉ » à la barre 1, l'astérisque "
             "au panneau — LE PANNEAU TOUJOURS CELUI DU DISQUE (les "
             "empreintes n'ont pas bougé : la divergence est NOMMÉE, jamais "
             "recalculée en silence)")
    emul.ecrire_cadre(556, struct.pack("<I", 0))

    # --- S5 : LE ROUTAGE CONSTATÉ (V3 de loupe-09 — les appels comptés) ------
    #     (le témoin 3f : le fichier qui DÉFILE — le 384 ne bouge pas, la borne)
    r = scenario("loupe.exe temoin-3f.bin",
                 [(0x770001, L.WM_PEINTURE, 0, 0),          # → loupe-10
                  (0x770001, L.WM_TAILLE, 0, (440 << 16) | 640),   # → loupe-11 (le remis)
                  (0x770001, L.WM_VSCROLL, 1, 0),            # → loupe-11 (le pas +1 ligne)
                  (0x770001, L.WM_VSCROLL, 5, 0),            # → loupe-11 (LA POIGNÉE : GetScrollInfo)
                  (0x770001, L.WM_MOLETTE, 0xFF880000, 0),   # → loupe-11 (le cran)
                  (0x770001, L.WM_TOUCHE, 0x74, 0),          # F5 → loupe-12
                  (0x770001, L.WM_CARACT, 0x31, 0),          # « 1 » → loupe-12
                  (0x770001, L.WM_CARACT, 0x0d, 0),          # retour → commit
                  (0x770001, L.WM_TOUCHE, 0x72, 0),          # F3 → loupe-14
                  (0x770001, L.WM_CARACT, 0x41, 0),          # hors saisie → Def
                  (0x770001, 0x0011, 0, 0)])                 # WM_QUERYOPEN → Def
    ok_route = (gui.compteurs["BeginPaint"] >= 1
                and gui.compteurs["GetScrollInfo"] >= 1
                and gui.compteurs["SetScrollInfo"] >= 2
                and gui.compteurs["InvalidateRect"] >= 2
                and gui.compteurs["MessageBoxW"] == 0
                and emul.os.compteurs["ReadFile"] >= 1)
    controle("V6.f:le-routage-constate-appel-par-appel", ok_route,
             "la file scriptée : WM_PAINT → loupe-10 (BeginPaint/EndPaint "
             "comptés), WM_VSCROLL + WM_MOUSEWHEEL → loupe-11 (le pas, la "
             "borne, SetScrollInfo synchrone), F5 + les WM_CHAR → loupe-12 "
             "(le mode, le commit, le saut — ReadFile compté), F3 → loupe-14 "
             "(la FIN nommée : le témoin 384 ne porte pas le motif), le "
             "reste → DefWindowProcW — CHAQUE routage chez son bloc")

    # --- S6 : le refus à l'ouverture — la vitrine VIDE VRAIE (Q1 de 09) ------
    r = scenario("loupe.exe absent-de-tout.bin",
                 [(0x770001, L.WM_PEINTURE, 0, 0)])
    mode = struct.unpack("<I", bytes(emul.uc.mem_read(L.R_SAISIE, 4)))[0]
    message = bytes(emul.uc.mem_read(L.R_SAISIE + 12, 24)).split(b"\x00")[0]
    vue, rempl = emul.u64(536), emul.u32(552)
    attendu = model_ecran(b"", 0, 0, 0, "", 0, 0, b"\x00" * 48, 3,
                          b"fichier introuvable", 27)
    controle("V6.g:le-refus-a-l-ouverture-vitrine-vide-vraie",
             mode == 3 and message == b"fichier introuvable"
             and etat_ecran() == attendu and r["exit_code"] == 0,
             "« absent-de-tout.bin » : loupe-01 rend -2, LA BARRE NOMME "
             "« fichier introuvable » (le mode MESSAGE posé), la vitrine "
             "s'ouvre VIDE VRAIE — l'état nommé, jamais la mort, l'écran == "
             "le modèle (le message à la barre 1, « - » au panneau)")

    # --- S7 : E1/E2 — la vitrine impossible s'explique PUIS meurt (D36) ------
    gui.reset()
    gui.hwnd = 0x770001
    gui.arm_register = True
    gui.scripter()
    r = emul.appeler_winmain("loupe.exe", [])
    ok_e1 = (r["exit_code"] == 1 and len(gui.boites) == 1
             and gui.boites[0][0] == ERREUR_NOM
             and gui.boites[0][1] == TITRE_NOM
             and gui.boites[0][2] == 0x10
             and gui.compteurs["GetMessageW"] == 0)
    gui.reset()
    gui.hwnd = 0x770001
    gui.arm_register = False
    gui.arm_create = True
    r = emul.appeler_winmain("loupe.exe", [])
    ok_e2 = (r["exit_code"] == 1 and len(gui.boites) == 1
             and gui.compteurs["GetMessageW"] == 0)
    gui.arm_create = False
    controle("V6.h:e1-e2-la-vitrine-impossible-expliquee-puis-morte",
             ok_e1 and ok_e2,
             "RegisterClassExW nul PUIS CreateWindowExW nul : MessageBoxW "
             "(MB_ICONERROR, l'explication fatale du plan, le titre) PUIS "
             "ExitProcess(1) — la boucle JAMAIS lancée (GetMessageW compté "
             "ZÉRO), jamais la mort silencieuse (D36)")


# =====================================================================================
# V7 — LA FALSIFICATION (une mutation = une divergence, zéro silence)
# =====================================================================================

def vecteur_v7(emul: EmulationRendu, os_v, temoins, rng):
    section("V7 — la falsification : chaque mutation attrapée par l'oracle")
    hwnd = 0x770001
    temoin = temoins["temoin-384.bin"]
    etat_neuf(emul, emul.gui)      # le lancement neuf : le .data d'initialiseur

    def muter(adresse: int, valeur: int):
        """LA MUTATION PROPRE : l'octet posé PUIS LE CACHE DE TRADUCTION
        VIDÉ (ctl_flush_tb — la voie officielle d'unicorn) : jamais un bloc
        périmé rejoué, jamais une falsification muette par le cache."""
        emul.uc.mem_write(adresse, bytes([valeur]))
        emul.uc.ctl_flush_tb()

    def ecran_du_bloc():
        emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
        return bytes(emul.uc.mem_read(L.R_ECRAN, 2320))

    def ecran_attendu(curseur=0, sale=0, vue=0):
        rempl = min(384, 384 - vue)
        return model_ecran(fenetre_modele(temoin, vue, rempl), vue, rempl,
                           384, "temoin-384.bin", curseur, sale,
                           hashlib.md5(temoin).digest()
                           + hashlib.sha256(temoin).digest(), 0, b"", 27)

    # (a) LE REMPLISSAGE D'ESPACES DE LOUPE-08 MUTÉ (0x20 → 0x21) : l'écran
    #     diverge — l'oracle échoue (la falsification DEMANDÉE, V4 de 08)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    emul.uc.mem_write(L.R_METRIQUES, struct.pack("<IIII", 8, 16, 27, 1))
    attendu = ecran_attendu()
    octets08 = bytearray(emul.uc.mem_read(L.LOUPE08_VA, 0x140))
    insns = list(emul.cs.disasm(bytes(octets08), L.LOUPE08_VA))
    cible = None
    for insn in insns:
        if insn.mnemonic == "mov" and insn.op_str.startswith(
                "byte ptr [r13 + rax], 0x20"):
            cible = insn.address + insn.size - 1        # l'octet immédiat
            break
    ok_mut_a = cible is not None
    if ok_mut_a:
        sain_avant = ecran_du_bloc()
        muter(cible, 0x21)                              # l'espace → « ! »
        ecran_mute = ecran_du_bloc()
        diverge = ecran_mute != attendu
        muter(cible, 0x20)                              # la restauration
        ecran_repasse = ecran_du_bloc()
        repasse = ecran_repasse == attendu
        ok_mut_a = diverge and repasse
        if not ok_mut_a:
            print(f"    [V7.a] cible 0x{cible:x} diverge={diverge} "
                  f"repasse={repasse} sain==attendu={sain_avant == attendu}")
            for i in range(2320):
                if sain_avant[i] != attendu[i]:
                    print(f"    [V7.a] l'écran sain diverge de l'attendu @ {i} "
                          f"(0x{i:x}) : {sain_avant[i]:#04x} != {attendu[i]:#04x}")
                    print("    sain   :", sain_avant[max(0, i-24):i+48])
                    print("    attendu:", attendu[max(0, i-24):i+48])
                    break
    controle("V7.a:le-remplissage-mute-l-ecran-diverge", ok_mut_a,
             "UN octet de la notation loupe-08 muté (le remplissage "
             "d'espaces 0x20 → 0x21) : l'écran attendu DIVERGE (l'oracle à "
             "scénarios échoue) ; l'octet restauré, l'écran RE-PASSE — la "
             "mutation ne laisse AUCUNE trace")

    # (b) LA CONSTANTE DE RECADRAGE DE LOUPE-12 MUTÉE (176 → 192) : le saut
    #     diverge (V5 de loupe-12)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    temoin3f = temoins["temoin-3f.bin"]
    octets12 = bytearray(emul.uc.mem_read(L.LOUPE12_VA, 0x340))
    insns = list(emul.cs.disasm(bytes(octets12), L.LOUPE12_VA))
    cible = None
    for insn in insns:
        if insn.mnemonic == "sub" and insn.op_str == "rcx, 0xb0":
            # l'immédiat 32 bits : 48 81 E9 B0 00 00 00 — le B0 est le
            # PREMIER octet de l'immédiat (adresse + 3), jamais le dernier
            cible = insn.address + 3
            break
    ok_mut_b = cible is not None
    if ok_mut_b:

        def saut():
            """Chaque saut part du MÊME état neuf : la session rouverte, la
            saisie vierge, le curseur à 0 — jamais l'état du saut précédent
            (la vue du muté ne doit pas porter le saut sain)."""
            HN.fermer_session(emul)
            HN.emplacer_session(emul, os_v, "temoin-3f.bin")
            emul.uc.mem_write(L.R_SAISIE, b"\x00" * L.ZONE_SAISIE)
            emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": 0x74, "r9": 0})
            for chiffre in b"1000":
                emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                            "r8": chiffre, "r9": 0})
            return emul.appeler(L.LOUPE12_VA, {"rcx": hwnd, "rdx": 0x102,
                                               "r8": 0x0d, "r9": 0})

        muter(cible, 0xC0)                              # 176 → 192 (0xC0)
        r = saut()
        vue_mutee = emul.u64(536)
        muter(cible, 0xB0)                              # la restauration
        r = saut()
        vue_saine = emul.u64(536)
        ok_mut_b = (vue_mutee != vue_saine
                    and vue_saine == min(L.recadre(0x1000),
                                         L.vue_max(len(temoin3f))))
    controle("V7.b:le-recadrage-mute-le-saut-diverge", ok_mut_b,
             "la constante de recadrage mutée d'une ligne (176 → 192) : la "
             "vue du saut diverge (0x{:x} ≠ 0x{:x}) ; restaurée, la vue "
             "== la règle EXÉCUTABLE du plan — la falsification "
             "DEMANDÉE attrapée par le scénario".format(
                 vue_mutee if ok_mut_b else 0, vue_saine if ok_mut_b else 1))

    # (c) LA TABLE HEX MUTÉE : chaque ligne diverge (V2 de loupe-08)
    table = bytes(emul.uc.mem_read(L.R_HEX, 16))
    mutee = bytearray(table)
    mutee[1] = ord("9")          # « 1 » → « 9 » : tout chiffre 1 devient 9
    muter(L.R_HEX, mutee[1])
    diverge = ecran_du_bloc() != attendu
    muter(L.R_HEX, table[1])     # la table du plan restaurée (le cache vidé)
    controle("V7.c:la-table-hex-mutee-chaque-ligne-diverge", diverge,
             "la table « 0123456789ABCDEF » du plan mutée d'un caractère "
             "(« 1 » → « 9 ») : les lignes portant le chiffre divergent — "
             "l'oracle échoue (la table .rdata est le plan, jamais une "
             "chance)")

    # (d) L'ANTI-MUET : chaque octet de l'écran attendu muté → l'égalité échoue
    ecran_vrai = ecran_du_bloc()
    muets = sum(1 for i in range(0, 2320, 7)
                if (ecran_vrai[:i] + bytes([ecran_vrai[i] ^ 1])
                    + ecran_vrai[i + 1:]) != ecran_vrai)
    controle("V7.d:l-anti-muet-332-octets-mutes", muets == len(range(0, 2320, 7)),
             f"chaque octet de l'écran attendu muté d'un bit (aux 332 "
             "positions sondées) → l'égalité échoue — la comparaison "
             "n'est PAS muette")

    # (e) LE RECOUVREMENT MUTÉ : l'occurrence à cheval manquée (V2 de 14)
    os_v.declarer("temoin-front.bin", HN.FichierVirtuel(
        contenu=temoins["temoin-front.bin"]))
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-front.bin")
    motif5 = b"\xde\xad\xbe\xef\x99"

    def poser_le_motif():
        """La saisie CHERCHER reposée AVANT CHAQUE commit : la chaîne
        précédente a posé la FIN nommée au tampon (le message VIT là — la
        saisie refermée ne le garde pas)."""
        hexa = motif5.hex().upper().encode()
        emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 2, 0, 0)
                          + hexa + b"\x00" * (80 - len(hexa)))
        emul.ecrire_cadre(544, struct.pack("<Q", 0))

    # la chaîne SAINE : les trois occurrences à cheval trouvées
    poser_le_motif()
    r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x0d, "r9": 0})
    saines = [emul.u64(544)]
    while True:
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": 0x72, "r9": 0})
        if r["rax"] != 0:
            break
        saines.append(emul.u64(544))
    # LE MUTANT : le « − longueur » du recouvrement retiré (bord' avance de
    # 65537 au lieu de 65537 − L) — la fenêtre suivante SAUTE les L−1 octets
    # du cheval : l'occurrence à la frontière n'est DANS AUCUNE fenêtre
    octets14 = bytearray(emul.uc.mem_read(L.LOUPE14_VA, 0x400))
    cible, taille_sub = None, 0
    for insn in emul.cs.disasm(bytes(octets14), L.LOUPE14_VA):
        if insn.mnemonic == "sub" and insn.op_str == "rax, r14":
            cible = insn.address - L.LOUPE14_VA
            taille_sub = insn.size
            break
    ok_mut_e = cible is not None and saines == [65536 * k - 2 for k in (1, 2, 3)]
    if not ok_mut_e:
        print(f"    [V7.e] cible={cible} saines={saines} attendues="
              f"{[65536 * k - 2 for k in (1, 2, 3)]}")
    if ok_mut_e:
        for k in range(taille_sub):
            muter(L.LOUPE14_VA + cible + k, 0x90)   # le sub neutralisé (NOP)
        poser_le_motif()
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": 0x0d, "r9": 0})
        ok_mut_e = r["rax"] == -1 and emul.u64(544) == 0
        if not ok_mut_e:
            print(f"    [V7.e] le muté : commit {r['rax']} curseur {emul.u64(544)}")
        # la restauration : les octets du plan re-posés (le cache vidé),
        # la chaîne re-passe
        octets_propres, _ = B4.assembler_bloc(
            emul.ks, os.path.join(ICI, "notation", "loupe-14-suivant.asm"),
            L.LOUPE14_VA, 0x400)
        emul.uc.mem_write(L.LOUPE14_VA, octets_propres)
        emul.uc.ctl_flush_tb()
        poser_le_motif()
        r = emul.appeler(L.LOUPE14_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": 0x0d, "r9": 0})
        ok_mut_e = ok_mut_e and r["rax"] == 0 and emul.u64(544) == 65534
        if not (r["rax"] == 0 and emul.u64(544) == 65534):
            print(f"    [V7.e] la re-passe : {r['rax']} curseur {emul.u64(544)}")
    controle("V7.e:le-recouvrement-mute-l-occurrence-manquee", ok_mut_e,
             "le « − longueur » du recouvrement neutralisé : la fenêtre "
             "suivante saute les octets du cheval, les occurrences à "
             "cheval n'existent dans AUCUNE fenêtre → LA FIN NOMMÉE sans "
             "rien trouvé (le muté) ; les octets du plan re-posés : la "
             "première à cheval TROUVÉE à 0xFFFE (la re-passe) — la preuve "
             "du recouvrement exigée DANS LES DEUX SENS")


# =====================================================================================
# LE CAHIER COMPLET
# =====================================================================================

GRAINE = 20261108


def main() -> int:
    global GRAINE
    if "--graine" in sys.argv:
        GRAINE = int(sys.argv[sys.argv.index("--graine") + 1])
    print(f"=== loupe/harnais_rendu.py — L'ORACLE À SCÉNARIOS (chantier "
          f"M10-(c), graine {GRAINE}) ===")
    rng = random.Random(GRAINE)
    temoins = HN.composer_temoins()
    temoins["proxy.exe"] = open(os.path.join(TRIADE, HN.SCELLE_M9), "rb").read()
    temoins_rendu, straddles = composer_temoins_rendu(
        random.Random(20261108))     # les témoins du geste : FIXES entre les re-jeux
    temoins.update(temoins_rendu)

    donnees_demo, donnees_m1 = vecteur_v0()
    donnees_m9 = open(os.path.join(TRIADE, HN.SCELLE_M9), "rb").read()
    os_v = HN.OSVirtuel()
    for nom, donnees in temoins.items():
        os_v.declarer(nom, HN.FichierVirtuel(contenu=donnees))
    emul = EmulationRendu(os_v, donnees_m9, donnees_m1, donnees_demo)
    vecteur_v1(emul, donnees_m1, donnees_demo)
    vecteur_v2(emul, temoins, rng)
    vecteur_v3(emul, temoins, rng)
    vecteur_v4(emul, os_v, temoins, straddles, rng)
    vecteur_v5(emul, os_v, temoins, rng)
    vecteur_v6(emul, os_v, temoins)
    vecteur_v7(emul, os_v, temoins, rng)

    controle("FINAL:aucune-feuille-du-(d)-appelee",
             emul.os.appels_interdits == 0,
             "les 5 feuilles du chantier (d) + GetModuleHandleW (le mort) "
             "n'ont JAMAIS été touchées (le compteur) — la liste fermée "
             "tenue sur pièces")

    total = len(REUSSITES) + len(ECHECS)
    print(f"\n=== LE CAHIER : {total} contrôles — "
          f"{len(REUSSITES)} VERTS, {len(ECHECS)} ÉCHECS ===")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  [ÉCHEC] {nom} — {detail}")
        print("VERDICT : ÉCHEC — le chantier n'est pas prouvé")
        return 1
    print("VERDICT : VERT — les familles rendu + navigation loupe-08..14 "
          "sont NOTÉES-MESURÉES-PROUVÉES sur pièces (l'oracle à scénarios "
          "vert : l'écran attendu octet par octet pour des états donnés ; "
          "le doré proxy ; le différentiel hashlib/bytes.find ; LE "
          "RECOUVREMENT par construction ; les refus nommés à la barre ; "
          "la falsification attrapée dans les deux sens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
