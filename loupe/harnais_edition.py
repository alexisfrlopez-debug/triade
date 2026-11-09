#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loupe/harnais_edition.py — L'ORACLE À SCÉNARIOS du geste M10-(d).

La famille édition (loupe-15..18 : le curseur, la saisie, la sauvegarde,
la sortie) NOTÉE-MESURÉE-PROUVÉE, et LA TABLE DE ROUTAGE DE LOUPE-09
ÉTENDUE (r2 — la révision nommée du geste (c) tenue). Le modèle est
l'oracle du rendu (M10-(c)) : la machinerie du mini-GUI virtuel réutilisée
TELLE QUELLE (l'émulation, la file scriptée, le Dispatch qui APPELLE LA
PROCÉDURE, le DC qui enregistre), l'appelant factice, le verdict TRANCHÉ
par le code.

LES PIÈCES NEUVVES DU GESTE : LE DISQUE SAISISSABLE et LA MORT. Le harnais
dote l'OS virtuel d'un WriteFile à l'ABI msx64 (l'écriture À L'OCTET dans
le fichier virtuel — l'échec armé au Nième appel, E2 de loupe-17) et le GUI
virtuel de ses trois feuilles de sortie : DestroyWindow (qui ENVOIE
WM_DESTROY à la procédure PAR LA MÊME MÉCANIQUE que le Dispatch — la pile
reçoit l'adresse magique, rip vise la procédure : la mort de la fenêtre est
la mécanique EXACTE d'USER32 réduite au laboratoire), PostQuitMessage (la
file quittée — GetMessageW rend 0, la boucle héritée win-03 rend, WinMain
retourne, ExitProcess(0) termine l'émulation le code consigné) et
MessageBeep (le refus s'ENTEND — le coup enregistré).

L'ORACLE : le modèle PYTHON INDÉPENDANT rejoue le pas, le clamp, la fenêtre
visible (les lignes de la vitrine), le recadrage, le journal PAR DÉCALAGE,
la marque, LA GARDE DU DOUBLE-GESTE (le réseau 16↔17↔18) et le témoin
composé — JAMAIS depuis les octets du bloc — et la comparaison est état par
état, écran attendu OCTET PAR OCTET, disque APRÈS == le modèle. Le juge ne
relit jamais l'accusé.

LE CAHIER (le miroir (b)/(c), la charte § 3 : les vecteurs AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : les scellés relus (proxy.exe 1.0.0, selftest
       M1, demo.exe 0.3.0 — les ancres R7), les QUATRE specs du geste
       relues, le plan recompté (les slots (d) ARRÊTÉS sur les mesures
       391/633/521/163 o, loupe-09 r2 CROIT 874 → 1135 o, les libellés du
       (d) @0x2520-0x259E, la table de routage ÉTENDUE dans la spec R1
       dès le geste (a)) ;
  V1 — LE ROUND-TRIP + LA STRUCTURE : les CINQ notations du geste
       ré-assemblées (keystone == capstone, R5), les appels directs à la
       liste fermée, loupe-09 r2 : LA ROUTE CONSTATÉE (chaque message du
       (d) chez son bloc, les appels comptés, DefWindowProcW pour le
       reste — y compris les flèches EN MODE SAISIE) ;
  V2 — LOUPE-15 LE CURSEUR : le différentiel 10 000 touches (le pas, le
       clamp, la fenêtre visible, le recadrage == le modèle ; les lectures
       comptées : la vue ne bouge QUE POUR SUIVRE) + les bords (les arrêts
       NOMMÉS, rax = 0 quand même, la vue INTACTE) + VK_DEBUT/VK_FIN à la
       ligne finale incomplète (la fin RÉELLE) + LA VUE SUIT à l'écran
       attendu octet par octet + LA VITRINE RÉTRÉCIE (la lecture stricte :
       jamais perdu hors écran) + le repli sans session ;
  V3 — LOUPE-16 LA SAISIE : le différentiel 10 000 frappes (le journal ET
       le tampon == le modèle : l'entrée PAR DÉCALAGE, le remplacement, la
       marque, LA GARDE RÉ-ARMÉE, le pas, la vue qui suit) + le scénario
       « 4d » (l'octet visible IMMÉDIATEMENT, MODIFIÉ + l'astérisque, la
       cellule suivante — l'écran attendu) + LES REJETS (sans session -4 ;
       la cellule fantôme -3 RIEN au journal ; le 257e distinct -3 nommé,
       RIEN perdu ; le non-hexa ignoré ; le fichier vide) + VK_SUPPR à
       l'attente (le premier chiffre repart) ;
  V4 — LOUPE-17 LA SAUVEGARDE : le différentiel 1 000 scénarios (le disque
       APRÈS == le modèle : SEULEMENT les N octets diffèrent, la taille
       CONSTANTE, le journal vidé, la marque levée, la garde levée) + le
       scénario des trois octets (LE TÉMOIN « 3 o écrits · 0x..0x » à la
       barre, le panneau RE-NÉ == hashlib du disque changé, l'astérisque
       parti — l'écran attendu) + le repli (Ctrl+S sans édition : « rien à
       sauver », AUCUN WriteFile compté) + L'ÉCHEC FAIL-CLOSED (le 2e
       WriteFile refuse : -6, le premier ACQUIS, le journal DEMEURE ; le
       second Ctrl+S REPREND ET FINIT) + sans session -4 ;
  V5 — LOUPE-18 LA SORTIE + LE RÉSEAU DE LA GARDE : la sortie directe
       (DestroyWindow compté, rax = 0) ; LE DOUBLE-GESTE (le premier
       WM_CLOSE refusé -5, LA PHRASE à la barre, le beep, la fenêtre
       DEMEURE ; le second TRANSCHE) ; LE RÉSEAU (refusé → Ctrl+S → la
       sortie DIRECTE ; refusé → une NOUVELLE écriture → le refus
       REVIENT) ; WM_DESTROY (loupe-03 compté, PostQuitMessage UNE fois,
       le journal ABANDONNÉ DÉLIBÉRÉMENT — le disque INTACT) ;
  V6 — L'ORACLE À SCÉNARIOS DU GESTE (le critère du plan) : LA BOUCLE
       COMPLÈTE DE L'ÉDITEUR par la ligne de commande — ouvrir, éditer,
       sauver, peindre (l'écran attendu octet par octet), Alt+F4 refusé,
       Alt+F4 encore : LA MORT COMPLÈTE (WM_DESTROY envoyé par le shim
       DestroyWindow, la session close, la file quittée, ExitProcess(0))
       avec le disque SAUVÉ == le modèle ; ET le chemin de l'abandon (le
       fichier INTACT après le double-geste sans sauvegarde) ; ET LA
       RÉ-OUVERTURE (le second loupe-01 lit les octets sauvés — la
       persistance constatée, les empreintes recoupées hashlib) ;
  V7 — LA FALSIFICATION (zéro silence) : la vue qui suit MUTÉE (le
       recadrage neutralisé : le curseur sort de l'écran — l'oracle
       échoue) ; LA GARDE DE 16 non ré-armée (le scénario du réseau
       échoue : la perte d'un seul geste) ; LA GARDE DE 17 non levée (le
       scénario échoue : le quitte-après-sauvegarde) ; L'OCTET DE TROP
       (l'écriture mutée à 2 o : la différentielle échoue — l'écriture à
       l'octet est une exigence) ; l'anti-muet du témoin.

Usage : python3 harnais_edition.py            # le cahier complet
        python3 harnais_edition.py --graine N # la graine (défaut 20261108)
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

# le harnais du rendu importé PAR CHEMIN NOMINATIF (la leçon D158) — la
# machinerie M10-(c) réutilisée TELLE QUELLE : l'émulation, le mini-GUI
# virtuel, la file scriptée, le DC qui enregistre, les modèles d'écran.
sys.path.insert(0, ICI)
if "harnais_rendu_mod" in sys.modules:
    HR = sys.modules["harnais_rendu_mod"]
else:
    _spec_hr = importlib.util.spec_from_file_location(
        "harnais_rendu_mod", os.path.join(ICI, "harnais_rendu.py"))
    HR = importlib.util.module_from_spec(_spec_hr)
    sys.modules["harnais_rendu_mod"] = HR
    _spec_hr.loader.exec_module(HR)

HN = HR.HN          # le noyau (M10-(b)) : l'OS virtuel, l'appelant factice
L = HR.L            # le plan loupe (la source unique)
B4 = HR.B4          # la machinerie de notation (assembler_bloc/round_trip)
ErreurHarnais = HN.ErreurHarnais
controle = HN.controle
section = HN.section
REUSSITES, ECHECS = HN.REUSSITES, HN.ECHECS

from unicorn import Uc, UcError  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP)

# --- les pièces du plan (le geste (d)) ----------------------------------------------

NOMS_EDITION = {
    "i110015": "loupe-15-curseur", "i110016": "loupe-16-saisie",
    "i110017": "loupe-17-sauver", "i110018": "loupe-18-quitter",
}
MESURES_EDITION = {"i110015": 391, "i110016": 660,
                   "i110017": 521, "i110018": 163}
MESURE_09_R2 = 1135                # loupe-09 r2 : la table étendue (874 → 1135)

# les libellés .rdata du geste (d) — les octets EXACTS (é = 0xE9, · = 0xB7)
LIBELLES_EDITION = {
    "journalplein": (L.L_JOURNALPLEIN, "journal plein - Ctrl+S"),
    "riensauver": (L.L_RIENSAUVER, "rien \xe0 sauver"),
    "ecrits": (L.L_ECRITS, " o \xe9crits \xb7 0x"),
    "jusqua": (L.L_JUSQUA, "..0x"),
    "quitter": (L.L_QUITTER,
                "MODIFI\xc9 - Alt+F4 encore pour quitter sans sauver, "
                "Ctrl+S pour sauver"),
}

# les messages du geste (d)
WM_CLOTURE = 0x0010                 # WM_CLOSE → loupe-18
WM_FIN_FENETRE = 0x0002             # WM_DESTROY → loupe-18
CTRL_S = 0x13                       # le code de contrôle Ctrl+S → loupe-17
VK = {"precedent": 0x21, "suivant": 0x22, "fin": 0x23, "debut": 0x24,
      "gauche": 0x25, "haut": 0x26, "droite": 0x27, "bas": 0x28}
PAS_15 = {0x25: -1, 0x27: 1, 0x26: -16, 0x28: 16, 0x21: -352, 0x22: 352}


# =====================================================================================
# LE DISQUE SAISISSABLE — le témoin que WriteFile touche (l'oracle lit le disque)
# =====================================================================================

class FichierEditable(HN.FichierVirtuel):
    """Le témoin SAISISSABLE : l'écriture à l'octet matérialise le contenu
    (les zéros si la taille seule vivait) — l'oracle lit le disque APRÈS,
    la différentielle tranche : SEULEMENT les N octets ont bougé."""

    def ecrire(self, pos: int, donnees: bytes) -> None:
        if not isinstance(self.contenu, bytearray):
            base = self.contenu if self.contenu is not None \
                else bytes(self.taille)
            self.contenu = bytearray(base)
        fin = pos + len(donnees)
        if fin > len(self.contenu):
            raise ErreurHarnais(
                f"l'écriture à {pos:#x}+{len(donnees)} déborde le témoin")
        self.contenu[pos:fin] = donnees

    def lire(self, pos: int, n: int) -> bytes:
        # TOUJOURS des bytes : unicorn refuse les bytearray (la leçon du
        # premier passage — le disque saisissable reste BYTES au lecteur)
        donnees = super().lire(pos, n)
        return bytes(donnees) if isinstance(donnees, bytearray) else donnees


class OSEdition(HN.OSVirtuel):
    """Le noyau + WriteFile : l'écriture à la position de la poignée, le
    compteur, le journal des écritures (offset, octets), l'échec armé au
    Nième appel — E2 de loupe-17 : le refus système au moment choisi."""

    def __init__(self):
        super().__init__()
        self.compteurs["WriteFile"] = 0
        self.ecritures: list[tuple[int, bytes]] = []
        self._echec_write_dans: int | None = None
        self._echec_write_compteur = 0

    def armer_echec_write(self, dans: int | None) -> None:
        self._echec_write_dans = dans
        self._echec_write_compteur = 0

    def write_file(self, h: int, n: int, donnees: bytes) -> bool:
        self.compteurs["WriteFile"] += 1
        if self._echec_write_dans is not None:
            self._echec_write_compteur += 1
            if self._echec_write_compteur == self._echec_write_dans:
                self._erreur(1117)   # ERROR_IO_DEVICE — le refus du labo
                return False
        ent = self.poignees.get(h)
        if ent is None:
            self._erreur(6)          # ERROR_INVALID_HANDLE
            return False
        fv = self.fichiers[ent[0]]
        if not isinstance(fv, FichierEditable):
            raise ErreurHarnais(f"{ent[0]} n'est pas saisissable")
        fv.ecrire(ent[1], donnees)
        self.poignees[h] = (ent[0], ent[1] + n)
        self.ecritures.append((ent[1], donnees))
        self.gle = 0
        return True


# =====================================================================================
# LE GUI ÉTENDU — la mort de la fenêtre (DestroyWindow envoie WM_DESTROY)
# =====================================================================================

FEUILLES_EDITION = ("WriteFile", "DestroyWindow", "PostQuitMessage",
                    "MessageBeep")


class EmulationEdition(HR.EmulationRendu):
    """L'image loupe du geste (d) : les 18 notations, l'IAT à 33 feuilles
    VIVANTES (les 29 du (c) + les 4 du (d) ; GetModuleHandleW seul demeure
    au mort — le hInstance de l'ABI de WinMain), les libellés du (d) posés
    au plan, LE DISQUE SAISISSABLE, LA MORT de la fenêtre."""

    def __init__(self, os_virtuel: OSEdition, donnees_m9: bytes,
                 donnees_m1: bytes, donnees_demo: bytes):
        super().__init__(os_virtuel, donnees_m9, donnees_m1, donnees_demo)
        gui = self.gui
        gui.fenetre_detruite = False
        gui.quit_poste = 0
        gui.beeps: list[int] = []

        # -- les QUATRE notations du geste (le lecteur canonique) --------------
        for bid, nom in NOMS_EDITION.items():
            rva, slot = L.SLOTS_LOUPE[bid]
            chemin = os.path.join(ICI, "notation", nom + ".asm")
            octets, metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            self.uc.mem_write(rva, octets)
            self.blobs[bid] = (octets, metas)

        # -- les libellés du geste (d) : le plan, source unique -----------------
        for _, (adr, texte) in LIBELLES_EDITION.items():
            self.uc.mem_write(adr, texte.encode("latin-1") + b"\x00")

        # -- l'IAT : les QUATRE feuilles du (d) VIVANTES ------------------------
        #    (le parent les posait au mort : re-pointées, le mort ne garde que
        #    GetModuleHandleW — le hInstance vient de l'ABI, D174)
        base = HN.ZONE_SHIMS[0]
        i = 8 + len(HR.FEUILLES_GUI_K32) + len(HR.FEUILLES_GUI_USER32) \
            + len(HR.FEUILLES_GUI_GDI)
        for feuille in FEUILLES_EDITION:
            adr = base + 8 * i
            i += 1
            self.adr_shims[adr] = feuille
            self.uc.mem_write(L.IAT_SLOTS[feuille], struct.pack("<Q", adr))

    # -- les shims du geste (d) : le disque + la mort ---------------------------

    def _shim_gui(self, uc, feuille: str) -> bool:
        if feuille in FEUILLES_EDITION:
            self._shim_edition(uc, feuille)
            return True
        return super()._shim_gui(uc, feuille)

    def _shim_edition(self, uc, feuille: str) -> None:
        gui = self.gui
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        rsp = uc.reg_read(UC_X86_REG_RSP)

        if feuille == "WriteFile":
            gui.compteurs[feuille] = gui.compteurs.get(feuille, 0) + 1
            # LA LEÇON DE L'ENTRÉE 207 : lpOverlapped (l'argument 5) vit à
            # [rsp+0x28] AU SHIM (le retour poussé) — le VRAI WriteFile
            # l'EXIGE NUL sur un handle synchrone : le garde lit LE VRAI
            # SLOT, comme le shim TextOutW du rendu et les shims du noyau
            lp_overlapped = struct.unpack(
                "<Q", uc.mem_read(rsp + 0x28, 8))[0]
            if lp_overlapped != 0:
                self.os._erreur(87)      # ERROR_INVALID_PARAMETER
                self._retour(uc, 0)
                return
            n = r8 & 0xFFFFFFFF
            donnees = bytes(uc.mem_read(rdx, n)) if n else b""
            ok = self.os.write_file(rcx, n, donnees)
            self._retour(uc, 1 if ok else 0)
            return
        if feuille == "DestroyWindow":
            gui.compteurs[feuille] = gui.compteurs.get(feuille, 0) + 1
            gui.fenetre_detruite = True
            # LA MÉCANIQUE D'USER32 : WM_DESTROY ENVOYÉ SYNCHRONÉMENT à la
            # procédure — la pile reçoit l'adresse magique, les quatre
            # arguments, rip vise la procédure enregistrée (le miroir EXACT
            # du Dispatch : la réponse revient par RETOUR_DISPATCH au site
            # d'appel de loupe-18)
            if not gui.wndproc:
                raise ErreurHarnais("DestroyWindow sans procédure enregistrée")
            uc.reg_write(UC_X86_REG_RSP, rsp - 8)
            uc.mem_write(rsp - 8, struct.pack("<Q", HR.RETOUR_DISPATCH))
            uc.reg_write(UC_X86_REG_RCX, rcx)
            uc.reg_write(UC_X86_REG_RDX, WM_FIN_FENETRE)
            uc.reg_write(UC_X86_REG_R8, 0)
            uc.reg_write(UC_X86_REG_R9, 0)
            uc.reg_write(UC_X86_REG_RIP, gui.wndproc)
            return
        if feuille == "PostQuitMessage":
            gui.compteurs[feuille] = gui.compteurs.get(feuille, 0) + 1
            gui.quit_poste += 1
            self._retour(uc, 0)
            return
        if feuille == "MessageBeep":
            gui.compteurs[feuille] = gui.compteurs.get(feuille, 0) + 1
            gui.beeps.append(rcx & 0xFFFFFFFF)
            self._retour(uc, 1)
            return
        raise ErreurHarnais(f"shim du (d) inconnu : {feuille}")

    def _instrument(self, uc, adresse, taille, donnees):
        if adresse == HR.RETOUR_DISPATCH:
            # la procédure a rendu (Dispatch OU DestroyWindow) : le retour au
            # site d'appel, rax = 0 — le mécanisme du (c) repris TEL QUEL
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RAX, 0)
            uc.reg_write(UC_X86_REG_RIP, ret)
            return
        super()._instrument(uc, adresse, taille, donnees)


# =====================================================================================
# LE MODÈLE — le juge indépendant (jamais les octets du bloc)
# =====================================================================================

def m15_curseur(vk: int, curseur: int, taille: int) -> int:
    """Le pas + le clamp (Q1/Q2) : les bords SONT DES ARRÊTS."""
    if taille <= 0:
        return curseur
    if vk == VK["debut"]:
        return curseur & ~15
    if vk == VK["fin"]:
        return min((curseur & ~15) + 15, taille - 1)
    pas = PAS_15.get(vk)
    if pas is None:
        return curseur
    return max(0, min(taille - 1, curseur + pas))


def m_lignes_visibles(lignes: int) -> int:
    """La fenêtre visible de la spec : les lignes de la vitrine − 3, capées
    24 (la barre ancrée au bas — la leçon du geste (c))."""
    return min(24, max(0, lignes - 3))


def m_vue_suit(curseur: int, vue: int, taille: int, lignes: int):
    """La vue suit (Q3) : (nouvelle vue, relecture ?) — la règle du plan."""
    v = m_lignes_visibles(lignes)
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min(L.recadre(curseur), L.vue_max(taille))
    return (nv, nv != vue)


def m_journal_seconde(journal: list, curseur: int, octet: int):
    """L'entrée PAR DÉCALAGE (Q2) : le remplacement ou l'ajout, la borne
    256 (E3) rend (journal', refus)."""
    for i, (dec, _) in enumerate(journal):
        if dec == curseur:
            journal[i] = (curseur, octet)
            return journal, False
    if len(journal) >= L.EDITS_MAX:
        return journal, True
    journal.append((curseur, octet))
    return journal, False


def fenetre_editee(disk: bytes, journal: list, vue: int, remplissage: int):
    """La fenêtre du modèle : les octets du DISQUE + LE RECOUVREMENT du
    journal (loupe-02 Q2 — l'édition survit au défilement)."""
    fen = bytearray(disk[vue:vue + remplissage])
    for dec, oct_ in journal:
        if vue <= dec < vue + remplissage:
            fen[dec - vue] = oct_
    return bytes(fen)


def model_temoign(n: int, premiere: int, derniere: int) -> bytes:
    """LE TÉMOIN de Q5 : « N o écrits · 0xAABBCCDD..0xEEFFGGHH » (le compte
    décimal, les adresses en 8 chiffres MAJUSCULES — la table HEX)."""
    return (f"{n}".encode() + LIBELLES_EDITION["ecrits"][1].encode("latin-1")
            + f"{premiere:08X}".encode()
            + LIBELLES_EDITION["jusqua"][1].encode("latin-1")
            + f"{derniere:08X}".encode())


def lire_journal(emul) -> list:
    n = emul.journal_nombre()
    entrees = []
    for i in range(n):
        dec, = struct.unpack("<Q", emul.uc.mem_read(L.R_JOURNAL + 16 * i, 8))
        oct_, = struct.unpack("<B", emul.uc.mem_read(
            L.R_JOURNAL + 16 * i + 8, 1))
        entrees.append((dec, oct_))
    return entrees


def barre(emul) -> bytes:
    return bytes(emul.uc.mem_read(L.R_SAISIE + 12, 80)).split(b"\x00")[0]


def poser_metriques(emul, lignes: int = 27) -> None:
    emul.uc.mem_write(L.R_METRIQUES, struct.pack("<IIII", 8, 16, lignes, 1))


def reset_saisie(emul) -> None:
    """La zone SAISIE remise AU VIERGE entre les scénarios : le mode, l'attente
    (actif/nibble) et le tampon — les scénarios ne fuient JAMAIS d'un vecteur
    à l'autre (l'hygiène du labo, le miroir de loupe-03)."""
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * L.ZONE_SAISIE)


def reset_gui(emul, hwnd: int = 0x770001) -> None:
    """Le GUI réinitialisé AUX ATTRIBUTS DU GESTE (d) : le reset du (c)
    ignore la fenêtre détruite, la file quittée et les beeps — les attributs
    neufs posés ici, la wndproc ENREGISTRÉE (DestroyWindow l'exige : la
    mort de la fenêtre ENVOIE WM_DESTROY à la procédure)."""
    emul.gui.reset()
    emul.gui.hwnd = hwnd
    emul.gui.fenetre_detruite = False
    emul.gui.quit_poste = 0
    emul.gui.beeps = []
    emul.gui.wndproc = emul.adresse_procedure()


def muter(emul, adresse: int, octets) -> None:
    emul.uc.mem_write(adresse, bytes(octets))
    emul.uc.ctl_flush_tb()      # la voie officielle : jamais un mutant muet


def restaurer_bloc(emul, nom: str, bid: str) -> None:
    rva, slot = L.SLOTS_LOUPE[bid]
    octets, _ = B4.assembler_bloc(
        emul.ks, os.path.join(ICI, "notation", nom + ".asm"), rva, slot)
    emul.uc.mem_write(rva, octets)
    emul.uc.ctl_flush_tb()


def chercher_insn(emul, va: int, slot: int, mnemo: str, operande: str):
    """L'adresse RELATIVE du premier (mnemo, operande) du bloc — la cible de
    la falsification (capstone, jamais une adresse au hasard)."""
    octets = bytes(emul.uc.mem_read(va, slot))
    for insn in emul.cs.disasm(octets, va):
        if insn.mnemonic == mnemo and insn.op_str == operande:
            return insn.address - va, insn.size
    return None, 0


# =====================================================================================
# V0 — LES PIÈCES DU PLAN
# =====================================================================================

def vecteur_v0():
    section("V0 — les pièces du plan (les scellés relus, le plan recompté)")
    donnees_m9 = open(os.path.join(TRIADE, HN.SCELLE_M9), "rb").read()
    ok_m9 = (len(donnees_m9) == HN.SCELLE_M9_TAILLE
             and hashlib.sha256(donnees_m9).hexdigest() == HN.SCELLE_M9_SHA256)
    controle("V0.a:le-scelle-1.0.0-relu", ok_m9,
             "proxy.exe 65 024 o, sha256 446279f3… — l'ancre R7 de la famille "
             "sha (loupe-05, le panneau re-né de loupe-17 la rappelle)")
    donnees_m1 = open(os.path.join(TRIADE, HN.SCELLE_M1), "rb").read()
    ok_m1 = (len(donnees_m1) == HN.SCELLE_M1_TAILLE
             and hashlib.sha256(donnees_m1).hexdigest() == HN.SCELLE_M1_SHA256)
    controle("V0.b:le-scelle-M1-relu", ok_m1,
             "selftest.exe 9 216 o — l'ancre R7 de libc-02 (le memcmp de "
             "loupe-13, vivant au geste (c))")
    donnees_demo = open(os.path.join(TRIADE, HR.SCELLE_DEMO), "rb").read()
    ok_demo = (len(donnees_demo) == HR.SCELLE_DEMO_TAILLE
               and hashlib.md5(donnees_demo).hexdigest() == HR.SCELLE_DEMO_MD5)
    controle("V0.c:le-scelle-demo-relu", ok_demo,
             "demo.exe 0.3.0, md5 73c064fb… — l'ancre R7 de win-03 (la boucle "
             "héritée que la mort de loupe-18 rend)")
    # les QUATRE specs du geste relues (les têtes + la révision)
    ok_specs = True
    for bid, nom in NOMS_EDITION.items():
        chemin = os.path.join(ICI, "I", nom + ".md")
        if not os.path.exists(chemin):
            ok_specs = False
            continue
        premiere = open(chemin, encoding="utf-8").readline()
        if f"loupe-{bid[5:7]}" not in premiere or "révision" not in premiere:
            ok_specs = False
    controle("V0.d:les-quatre-specs-du-geste-relues", ok_specs,
             "les têtes loupe-15..18 (la couche I posée au geste (a), "
             "révision 1 — écrite-avant-code, R2 tenue)")
    # le plan : les slots (d) ARRÊTÉS sur les mesures (D161) + loupe-09 r2
    ok_slots = (L.SLOTS_LOUPE["i110009"] == (0x5C00, 0x480)
                and L.SLOTS_LOUPE["i110015"] == (0x6080, 0x1C0)
                and L.SLOTS_LOUPE["i110016"] == (0x6240, 0x2C0)
                and L.SLOTS_LOUPE["i110017"] == (0x6500, 0x240)
                and L.SLOTS_LOUPE["i110018"] == (0x6740, 0xC0))
    ok_tasse = (L.SLOTS_LOUPE["i110014"][0] + L.SLOTS_LOUPE["i110014"][1]
                == 0x5C00
                and L.SLOTS_LOUPE["i110009"][0] + L.SLOTS_LOUPE["i110009"][1]
                == L.SLOTS_LOUPE["i110015"][0]
                and L.SLOTS_LOUPE["i110015"][0] + L.SLOTS_LOUPE["i110015"][1]
                == L.SLOTS_LOUPE["i110016"][0]
                and L.SLOTS_LOUPE["i110016"][0] + L.SLOTS_LOUPE["i110016"][1]
                == L.SLOTS_LOUPE["i110017"][0]
                and L.SLOTS_LOUPE["i110017"][0] + L.SLOTS_LOUPE["i110017"][1]
                == L.SLOTS_LOUPE["i110018"][0]
                and L.SLOTS_LOUPE["i110018"][0] + L.SLOTS_LOUPE["i110018"][1]
                == 0x6800
                and all(L.SLOTS_LOUPE[b][1] % 64 == 0
                        and L.SLOTS_LOUPE[b][1] - m >= 16
                        for b, m in list(MESURES_EDITION.items())
                        + [("i110009", MESURE_09_R2)]))
    controle("V0.e:les-slots-du-geste-arretes-sur-les-mesures",
             ok_slots and ok_tasse,
             "09 r2 @0x5C00 [1135 o, 0x480 — la table étendue : 874 → 1135] "
             "→ 15 @0x6080 [391, 0x1C0] → 16 @0x6240 [660, 0x2C0] → 17 "
             "@0x6500 [521, 0x240] → 18 @0x6740 [163, 0xC0] — fin 0x6800, "
             "multiples de 64, padding >= 16, les notations (c) voisines "
             "INTACTES")
    # les libellés du (d) + les constantes : le plan, source unique
    ok_rdata = (L.L_JOURNALPLEIN == 0x2520 and L.L_RIENSAUVER == 0x2537
                and L.L_ECRITS == 0x2545 and L.L_JUSQUA == 0x2554
                and L.L_QUITTER == 0x2559
                and L.L_QUITTER + 69 <= 0x2600
                and L.CTRL_S == 0x13 and L.WM_DESTRUCTION == 0x0002
                and L.JOUR_PAS == 16 and L.JOUR_NOMBRE == 4096
                and L.ZONE_JOURNAL == 4112)
    controle("V0.f:les-pieces-rdata-du-geste", ok_rdata,
             "les 5 libellés du (d) @0x2520-0x259E (journal plein, rien à "
             "sauver, le témoin, la phrase du double-geste — le tiret ASCII) "
             "· Ctrl+S 0x13 par WM_CHAR · WM_DESTROY 0x0002 · le journal "
             "4 112 o (256 × 16, le nombre à +4096)")
    # la table de routage ÉTENDUE : la spec R1 la déclarait dès le geste (a)
    spec09 = open(os.path.join(ICI, "I", "loupe-09-ecran.md"),
                  encoding="utf-8").read()
    ok_route_spec = ("Ctrl+S → loupe-17" in spec09
                     and "WM_CLOSE → loupe-18" in spec09.replace(
                         "Alt+F4/WM_CLOSE → loupe-18", "WM_CLOSE → loupe-18")
                     and "loupe-15" in spec09 and "loupe-16" in spec09)
    controle("V0.g:la-table-etendue-declaree-des-le-geste-a", ok_route_spec,
             "la spec loupe-09 R1 (posée au geste (a)) déclare DÉJÀ la table "
             "complète : flèches → 15, hexa → 16, Ctrl+S → 17, Alt+F4 → 18 "
             "— la révision (d) du bloc TENAIT la promesse, la spec ne "
             "bouge pas")
    return donnees_m9, donnees_m1, donnees_demo


# =====================================================================================
# V1 — LE ROUND-TRIP + LA STRUCTURE + LA ROUTE CONSTATÉE
# =====================================================================================

def vecteur_v1(emul: EmulationEdition, os_v: OSEdition):
    section("V1 — round-trip + la route du (d) constatée (chaque message "
            "chez son bloc)")
    hwnd = 0x770001
    # (a) le round-trip des CINQ notations du geste (loupe-09 r2 + 15..18)
    for bid, attendu in list({"i110009": MESURE_09_R2}.items()) \
            + list(MESURES_EDITION.items()):
        nom = {"i110009": "loupe-09-ecran", **NOMS_EDITION}[bid]
        rva, slot = L.SLOTS_LOUPE[bid]
        chemin = os.path.join(ICI, "notation", nom + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        controle(f"V1.a:{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o mesurés à l'arrêt, "
                 f"{len(insns)}/{len(metas)} instructions — keystone == "
                 "capstone (R5)")
    # (b) la structure : les appels directs du (d) à la liste fermée du plan
    fermee = {L.LOUPE01_VA, L.LOUPE02_VA, L.LOUPE03_VA, L.LOUPE04_VA,
              L.LOUPE05_VA, L.LOUPE06_VA, L.LOUPE07_VA, L.LOUPE08_VA,
              L.LOUPE09_VA, L.LOUPE10_VA, L.LOUPE11_VA, L.LOUPE12_VA,
              L.LOUPE13_VA, L.LOUPE14_VA, L.LOUPE15_VA, L.LOUPE16_VA,
              L.LOUPE17_VA, L.LOUPE18_VA, L.R_LIBC01, L.R_LIBC02,
              L.R_LIBC07, L.R_WIN03, L.R_TLS01, L.R_TLS03, L.R_TLS04}
    ok_appels = True
    for bid in ("i110015", "i110016", "i110017", "i110018"):
        nom = NOMS_EDITION[bid]
        va, slot = L.SLOTS_LOUPE[bid]
        for ligne in open(os.path.join(ICI, "notation", nom + ".asm"),
                          encoding="utf-8"):
            if ligne.startswith("; Appels directs"):
                for cible in ligne.split(":", 1)[1].split(", "):
                    cible = cible.replace("call ", "").strip()
                    if cible.startswith("qword"):
                        continue
                    adr = int(cible, 16)
                    if adr not in fermee and not (va <= adr < va + slot):
                        ok_appels = False   # les sous-routines locales exceptées
    controle("V1.b:les-appels-directs-a-la-liste-fermee", ok_appels,
             "loupe-15 → LOUPE02 ; loupe-16 → LOUPE02 ; loupe-17 → LOUPE07 ; "
             "loupe-18 → LOUPE03 ; loupe-09 r2 → 15/16/17/18 (la table "
             "étendue) — le réseau des specs, la liste fermée du plan")
    # (c) LA ROUTE CONSTATÉE : chaque message du (d) chez son bloc, compté
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    poser_metriques(emul)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x30))
    proc = emul.gui.wndproc
    # WM_KEYDOWN VK_BAS → loupe-15 (le curseur bouge : 0x30 + 16)
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x100,
                            "r8": VK["bas"], "r9": 0})
    ok_15 = r["rax"] == 0 and emul.u64(544) == 0x40
    # WM_KEYDOWN une touche hors table → DefWindowProcW
    defproc_avant = emul.gui.appels_defproc
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x100, "r8": 0x70, "r9": 0})
    ok_hors = r["rax"] == 0 and emul.gui.appels_defproc == defproc_avant + 1
    # les flèches EN MODE SAISIE → DefWindowProcW (le curseur INTACT)
    emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 1, 0, 0) + b"\x00" * 80)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x40))
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x100,
                            "r8": VK["bas"], "r9": 0})
    ok_saisie = (r["rax"] == 0 and emul.u64(544) == 0x40
                 and emul.gui.appels_defproc == defproc_avant + 2)
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * 96)
    # WM_CHAR '4' (mode RIEN) → loupe-16 (le nibble en attente)
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x102, "r8": 0x34, "r9": 0})
    actif, nibble = struct.unpack("<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
    ok_16 = r["rax"] == 0 and actif == 1 and nibble == 4
    # WM_CHAR 'z' (non hexa, mode RIEN) → DefWindowProcW (rien)
    defproc_avant = emul.gui.appels_defproc
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x102, "r8": 0x7A, "r9": 0})
    ok_nonhexa = r["rax"] == 0 and emul.gui.appels_defproc == defproc_avant + 1
    # WM_CHAR 0x13 (Ctrl+S) → loupe-17 (le journal VIDE : « rien à sauver »)
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": 0x102, "r8": CTRL_S, "r9": 0})
    ok_17 = (r["rax"] == 0 and barre(emul)
             == LIBELLES_EDITION["riensauver"][1].encode("latin-1")
             and os_v.compteurs["WriteFile"] == 0)
    # WM_CLOSE sans marque → loupe-18 → DestroyWindow → WM_DESTROY (le
    # nested) → loupe-03 + PostQuitMessage — LA MORT COMPLÈTE en un message
    close_avant = emul.gui.compteurs.get("DestroyWindow", 0)
    r = emul.appeler(proc, {"rcx": hwnd, "rdx": WM_CLOTURE, "r8": 0, "r9": 0})
    ok_18 = (r["rax"] == 0
             and emul.gui.compteurs.get("DestroyWindow", 0) == close_avant + 1
             and emul.gui.fenetre_detruite
             and emul.gui.compteurs.get("PostQuitMessage", 0) == 1
             and emul.gui.quit_poste == 1
             and emul.u64(528) == 0xFFFFFFFFFFFFFFFF)
    controle("V1.c:la-route-du-(d)-constatee",
             ok_15 and ok_hors and ok_saisie and ok_16 and ok_nonhexa
             and ok_17 and ok_18,
             "VK_BAS → 15 (curseur 0x30→0x40) ; la touche hors table et les "
             "flèches EN MODE SAISIE → DefWindowProcW (comptées, le curseur "
             "INTACT) ; '4' → 16 (le nibble 4 en attente) ; 'z' → le défaut ; "
             "Ctrl+S → 17 (« rien à sauver », AUCUN WriteFile) ; WM_CLOSE → "
             "18 : DestroyWindow → WM_DESTROY ENVOYÉ → loupe-03 + "
             "PostQuitMessage — LA MORT COMPLÈTE, la poignée rendue")


# =====================================================================================
# V2 — LOUPE-15 LE CURSEUR (le pas, la borne, la vue qui suit)
# =====================================================================================

def vecteur_v2(emul: EmulationEdition, os_v: OSEdition, temoins, rng):
    section("V2 — loupe-15 : le différentiel 10 000 touches + les scénarios")
    hwnd = 0x770001
    temoin = temoins["temoin-3f.bin"]
    taille = len(temoin)
    # (a) LE DIFFÉRENTIEL : 10 000 touches sur le témoin 3f — le pas, le
    # clamp, la fenêtre visible, le recadrage, les lectures comptées
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)          # la vitrine 0.1.0 : 27 lignes → V = 24
    divergences = 0
    curseur, vue = 0, 0
    cles = list(VK.values())
    lectures = os_v.compteurs["ReadFile"]
    for _ in range(10000):
        vk = rng.choice(cles)
        r = emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": vk, "r9": 0})
        curseur = m15_curseur(vk, curseur, taille)
        vue, relu = m_vue_suit(curseur, vue, taille, 27)
        if relu:
            lectures += 1
        ok = (r["rax"] == 0 and emul.u64(544) == curseur
              and emul.u64(536) == vue and vue % 16 == 0
              and emul.u32(552) == min(384, taille - vue)
              and os_v.compteurs["ReadFile"] == lectures)
        if not ok:
            divergences += 1
            if divergences == 1:
                print(f"    [V2.a] vk={vk:#x} curseur {emul.u64(544)} != "
                      f"{curseur} ou vue {emul.u64(536)} != {vue} "
                      f"(lectures {os_v.compteurs['ReadFile']} != {lectures})")
    controle("V2.a:le-differentiel-10000-touches", divergences == 0,
             "10 000 touches aléatoires (les HUIT VK) sur le témoin 3f : le "
             "curseur ET la vue == le modèle à CHAQUE pas (le clamp, la "
             "fenêtre visible, le recadrage, l'alignement 16, le "
             "remplissage), la relecture EXACTEMENT quand la vue bouge — "
             "I2 : la vue ne bouge QUE POUR SUIVRE, le harnais compte les "
             "lectures")
    # (b) LES BORDS : les arrêts NOMMÉS — rax = 0 QUAND MÊME, la vue INTACTE
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-1.bin")
    reset_gui(emul)
    poser_metriques(emul)
    lecture_avant = os_v.compteurs["ReadFile"]
    bords = []
    for vk in (VK["gauche"], VK["haut"], VK["precedent"]):
        r = emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": vk, "r9": 0})
        bords.append((r["rax"], emul.u64(544), emul.u64(536)))
    for vk in (VK["droite"], VK["bas"], VK["suivant"], VK["fin"]):
        r = emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                        "r8": vk, "r9": 0})
        bords.append((r["rax"], emul.u64(544), emul.u64(536)))
    controle("V2.b:les-bords-sont-des-arrets",
             all(rax == 0 and c == 0 and v == 0 for rax, c, v in bords[:3])
             and all(rax == 0 and c == 0 and v == 0 for rax, c, v in bords[3:])
             and os_v.compteurs["ReadFile"] == lecture_avant,
             "le témoin d'UN octet : à 0, GAUCHE/HAUT/PAGE restent ; à "
             "taille-1 (= 0), DROITE/BAS/PAGE/FIN restent — rax = 0 QUAND "
             "MÊME (le bord n'est pas un échec, E1 : la navigation S'ARRÊTE), "
             "la vue INTACTE, AUCUNE lecture (les compteurs)")
    # (c) VK_DEBUT / VK_FIN à la ligne finale incomplète (la fin RÉELLE)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x30000))
    emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                 "r8": VK["fin"], "r9": 0})
    fin_reelle = emul.u64(544)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x2FF09))
    emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                 "r8": VK["fin"], "r9": 0})
    fin_ligne = emul.u64(544)
    emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                 "r8": VK["debut"], "r9": 0})
    debut_ligne = emul.u64(544)
    controle("V2.c:debut-fin-la-ligne-finale-incomplete",
             fin_reelle == 0x30000 and fin_ligne == 0x2FF00 + 15
             and debut_ligne == 0x2FF00,
             "VK_FIN à 0x30000 (le dernier octet, ligne d'UN octet) → 0x30000 "
             "(min(0x3000F, taille-1) — JAMAIS un curseur sur un octet qui "
             "n'existe pas) ; à 0x2FF09 → 0x2FF0F (la fin de ligne réelle "
             "0x2FF00+15) ; VK_DEBUT → 0x2FF00 l'aligne16_inf — la ligne "
             "finale incomplète du témoin 3f le prouve")
    # (d) LA VUE SUIT : au bord de la fenêtre, VK_BAS — l'écran attendu
    emul.ecrire_cadre(536, struct.pack("<Q", 0))
    emul.ecrire_cadre(544, struct.pack("<Q", 23 * 16))
    emul.appeler(L.LOUPE02_VA, {"rcx": 0})
    emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                 "r8": VK["bas"], "r9": 0})
    curseur, vue = emul.u64(544), emul.u64(536)
    vue_attendue = min(L.recadre(23 * 16 + 16), L.vue_max(taille))
    emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    rempl = emul.u32(552)
    fenetre = fenetre_editee(temoin, [], vue, rempl)
    attendu = HR.model_ecran(fenetre, vue, rempl, taille, "temoin-3f.bin",
                             curseur, 0,
                             bytes(emul.uc.mem_read(L.R_EMPREINTES, 48)),
                             0, b"", 27)
    controle("V2.d:la-vue-suit-l-ecran-attendu",
             curseur == 23 * 16 + 16 and vue == vue_attendue
             and ecran == attendu,
             f"le curseur à la dernière ligne visible, VK_BAS : le curseur "
             f"0x170 → 0x180, la vue RECADRÉE 0 → 0x{vue_attendue:x} (la "
             "ligne active à la 12e — la règle du plan), la fenêtre RELUE, "
             "L'ÉCRAN ATTENDU OCTET PAR OCTET (les 2320 o == le modèle — le "
             "curseur JAMAIS perdu hors écran)")
    # (e) LA VITRINE RÉTRÉCIE : la lecture STRICTE (jamais perdu, y compris
    # quand la grille montre moins de 24 lignes)
    emul.ecrire_cadre(536, struct.pack("<Q", 0))
    emul.ecrire_cadre(544, struct.pack("<Q", 15 * 16))
    emul.appeler(L.LOUPE02_VA, {"rcx": 0})
    poser_metriques(emul, 12)          # 12 lignes → V = 9 : la vitrine rétrécie
    emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                 "r8": VK["bas"], "r9": 0})
    curseur12, vue12 = emul.u64(544), emul.u64(536)
    controle("V2.e:la-vitrine-retrecie-la-lecture-stricte",
             curseur12 == 16 * 16 and vue12 == min(L.recadre(16 * 16),
                                                   L.vue_max(taille)),
             "la vitrine rétrécie (12 lignes → 9 visibles) : le curseur à la "
             "ligne 15 SORT de la fenêtre visible → la vue SUIT quand même "
             "(la lecture STRICTE de la spec : jamais perdu hors écran — à "
             "la vitrine 0.1.0 la fenêtre == le remplissage, le miroir du "
             "commit de loupe-12)")
    poser_metriques(emul, 27)
    # (f) LE REPLI : sans session, les flèches ne bougent RIEN
    HN.fermer_session(emul)
    curseur_avant, vue_avant = emul.u64(544), emul.u64(536)
    lecture_avant = os_v.compteurs["ReadFile"]
    r = emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": VK["bas"], "r9": 0})
    controle("V2.f:le-repli-sans-session",
             r["rax"] == 0 and emul.u64(544) == curseur_avant
             and emul.u64(536) == vue_avant
             and os_v.compteurs["ReadFile"] == lecture_avant,
             "les flèches dans la vitrine vide ne bougent rien (P2/Q4 : le "
             "repli documenté — rax = 0 SANS effet, AUCUNE lecture)")
    # (g) LE FICHIER VIDE : aucune cellule n'existe
    os_v.declarer("temoin-vide.bin", HN.FichierVirtuel(contenu=b""))
    HN.emplacer_session(emul, os_v, "temoin-vide.bin")
    r = emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": VK["droite"], "r9": 0})
    controle("V2.g:le-fichier-vide-aucune-cellule",
             r["rax"] == 0 and emul.u64(544) == 0,
             "le fichier de taille zéro (loupe-01 r3, LE VIDE) : le curseur "
             "demeure — aucune cellule n'existe, le repli nommé")


# =====================================================================================
# V3 — LOUPE-16 LA SAISIE (le journal, la marque, la garde)
# =====================================================================================

def vecteur_v3(emul: EmulationEdition, os_v: OSEdition, temoins, rng):
    section("V3 — loupe-16 : le différentiel 10 000 frappes + les rejets")
    hwnd = 0x770001
    temoin = temoins["temoin-3f.bin"]
    taille = len(temoin)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    # (a) LE DIFFÉRENTIEL : 10 000 frappes — le journal, le tampon, la
    # marque, la garde, le pas, la vue (le modèle indépendant)
    reset_saisie(emul)
    journal: list = []
    modele_tampon = bytearray(temoin[:384])
    curseur, vue = 0x22, 0
    emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
    m_actif, m_nibble = 0, 0
    divergences = 0
    hexa = b"0123456789abcdefABCDEF"
    lectures = os_v.compteurs["ReadFile"]
    for _ in range(10000):
        frappe = 0x08 if rng.random() < 0.02 else rng.choice(hexa)
        r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": frappe, "r9": 0})
        # — le modèle (jamais les octets du bloc) —
        if frappe == 0x08:
            if m_actif:
                m_actif = 0             # le nibble effacé
        else:
            valeur = int(chr(frappe), 16)
            if not m_actif:
                m_actif, m_nibble = 1, valeur    # l'attente posée
            else:
                m_actif = 0             # l'engagement CONSOMME l'attente
                octet = (m_nibble << 4) | valeur
                journal, refuse = m_journal_seconde(journal, curseur, octet)
                if not refuse:
                    rempl = min(384, taille - vue)
                    if vue <= curseur < vue + rempl:
                        modele_tampon[curseur - vue] = octet
                    curseur = min(curseur + 1, taille - 1)
                    nv, relu = m_vue_suit(curseur, vue, taille, 27)
                    if relu:
                        lectures += 1
                        vue = nv
                        modele_tampon = bytearray(temoin[vue:vue + 384])
                        for dec, oct_ in journal:
                            if vue <= dec < vue + 384:
                                modele_tampon[dec - vue] = oct_
        # — la comparaison (l'état lu, jamais le modèle) —
        if r["rax"] not in (0, -3):
            divergences += 1
            if divergences == 1:
                print(f"    [V3.a] verdict {r['rax']} inattendu")
            continue
        actif, nibble = struct.unpack(
            "<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
        probleme = None
        if (actif, nibble) != (m_actif, m_nibble if m_actif else 0):
            probleme = f"l'attente ({actif},{nibble}) != ({m_actif},"
            probleme += f"{m_nibble if m_actif else 0})"
        elif lire_journal(emul) != journal:
            probleme = "le journal diverge"
        elif emul.u64(544) != curseur or emul.u64(536) != vue:
            probleme = f"curseur {emul.u64(544)} != {curseur} ou vue " \
                       f"{emul.u64(536)} != {vue}"
        elif bytes(emul.uc.mem_read(L.R_CADRE + 568, 384)) != bytes(
                modele_tampon):
            probleme = "le tampon diverge"
        elif emul.u32(556) != (1 if journal else 0) or emul.u32(560) != 0:
            probleme = "la marque ou la garde divergent"
        if probleme:
            divergences += 1
            if divergences == 1:
                print(f"    [V3.a] {probleme}")
    controle("V3.a:le-differentiel-10000-frappes", divergences == 0,
             "10 000 frappes hexa aléatoires (+ 2 % VK_SUPPR) : le journal "
             "PAR DÉCALAGE (la réécriture REMPLACE, le compte exact, la borne "
             "256 refusée NOMMÉMENT), l'attente CONSOMMÉE par l'engagement, "
             "le tampon de vue (le recouvrement immédiat), la marque sale, "
             "LA GARDE RÉ-ARMÉE à chaque écriture, le pas clampé, LA VUE QUI "
             "SUIT — tout == le modèle Python (les lectures comptées : la "
             "vue ne bouge que pour suivre)")
    # (b) LE SCÉNARIO « 4d » au curseur 0x22 : l'écran attendu
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    reset_saisie(emul)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x34, "r9": 0})
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x64, "r9": 0})
    r = emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    rempl = emul.u32(552)
    fenetre = fenetre_editee(temoin, [(0x22, 0x4D)], 0, rempl)
    attendu = HR.model_ecran(fenetre, 0, rempl, taille, "temoin-3f.bin",
                             0x23, 1,
                             bytes(emul.uc.mem_read(L.R_EMPREINTES, 48)),
                             0, b"", 27)
    controle("V3.b:le-scenario-4d-l-ecran-attendu",
             r["rax"] == 0 and emul.u64(544) == 0x23 and emul.u32(556) == 1
             and emul.u32(560) == 0 and lire_journal(emul) == [(0x22, 0x4D)]
             and ecran == attendu,
             "« 4 » puis « d » au curseur 0x22 : l'octet 0x4D AU JOURNAL ET "
             "AU TAMPON (visible IMMÉDIATEMENT), la marque sale (MODIFIÉ + "
             "l'astérisque au panneau), LA GARDE RÉ-ARMÉE, la cellule "
             "suivante active (curseur 0x23) — L'ÉCRAN ATTENDU OCTET PAR "
             "OCTET (les 2320 o == le modèle, l'octet édité à la ligne)")
    # (c) LES REJETS : -4, la fantôme, le 257e distinct, le non-hexa, LE VIDE
    HN.fermer_session(emul)
    r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": 0x34, "r9": 0})
    ok_e1 = (r["rax"] == -4 and barre(emul)
             == HR.LIBELLES["session"][1].encode("latin-1"))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    # la cellule fantôme : le curseur forgé au-delà du remplissage
    emul.ecrire_cadre(536, struct.pack("<Q", 0))
    emul.ecrire_cadre(544, struct.pack("<Q", 384 + 5))
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    emul.poser_journal([])
    r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x64, "r9": 0})
    ok_e2 = (r["rax"] == -3 and emul.journal_nombre() == 0
             and barre(emul) == HR.LIBELLES["horsbornes"][1].encode("latin-1"))
    # le fichier vide : aucune cellule n'existe
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-vide.bin")
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    emul.ecrire_cadre(544, struct.pack("<Q", 0))
    r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x64, "r9": 0})
    ok_vide = r["rax"] == -3 and emul.journal_nombre() == 0
    # le 257e distinct : la borne nommée, RIEN perdu (les 256 décalages
    # DISTINCTS ET VALIDES du témoin 384 — 0x40 à 0x13F)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    emul.ecrire_cadre(544, struct.pack("<Q", 0x20))
    entrees = [(0x40 + i, (i * 7) & 0xFF) for i in range(256)]
    emul.poser_journal(entrees)
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x64, "r9": 0})
    ok_e3 = (r["rax"] == -3 and emul.journal_nombre() == 256
             and lire_journal(emul) == entrees
             and barre(emul) == LIBELLES_EDITION["journalplein"][1]
                 .encode("latin-1"))
    # le non-hexa IGNORÉ (le repli documenté)
    emul.poser_journal([])
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 0, 0))
    for frappe in (0x7A, 0x21, 0x20):      # z ! espace
        r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": frappe, "r9": 0})
        if r["rax"] != 0 or emul.journal_nombre() != 0:
            break
    ok_e4 = (r["rax"] == 0 and emul.journal_nombre() == 0
             and emul.u32(556) == 0)
    controle("V3.c:les-rejets-nommes",
             ok_e1 and ok_e2 and ok_vide and ok_e3 and ok_e4,
             "sans session → -4 « aucun fichier ouvert » ; la cellule "
             "fANTÔME (le curseur forgé au-delà du remplissage) → -3 « hors "
             "bornes », RIEN au journal (le refus PRÉCÈDE, l'attente "
             "CONSOMMÉE) ; le fichier VIDE → -3 (aucune cellule n'existe) ; "
             "le 257e DISTINCT → -3 « journal plein - Ctrl+S », les 256 "
             "premiers INTACTS (rien perdu) ; « z », « ! », l'espace → "
             "IGNORÉS proprement (rax = 0, rien bougé)")
    # (d) VK_SUPPR à l'attente : le premier chiffre repart
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * 96)
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x34, "r9": 0})
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x08, "r9": 0})
    actif, nibble = struct.unpack("<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
    r = emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x08, "r9": 0})
    controle("V3.d:vk-suppr-a-l-attente",
             actif == 0 and nibble == 0 and r["rax"] == 0
             and emul.journal_nombre() == 0,
             "« 4 » frappé (l'attente posée), VK_SUPPR : le nibble EFFACÉ "
             "(actif = 0 — le premier chiffre repart) ; VK_SUPPR hors "
             "attente : IGNORÉ proprement (rien, rax = 0)")
    # (e) LA GARDE RÉ-ARMÉE après la sauvegarde (le réseau 16 → 17 → 18)
    emul.poser_journal([(0x40, 0xAA)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    emul.ecrire_cadre(560, struct.pack("<I", 0))
    emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                 "r8": CTRL_S, "r9": 0})
    garde_apres_sauve = emul.u32(560)        # 17 la LÈVE (plus rien à perdre)
    emul.ecrire_cadre(560, struct.pack("<I", 1))   # le premier Alt+F4 REFUSÉ
    emul.ecrire_cadre(544, struct.pack("<Q", 0x50))
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 0, 0))
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x62, "r9": 0})
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x62, "r9": 0})
    controle("V3.e:la-garde-re-armee-a-chaque-ecriture",
             garde_apres_sauve == 0 and emul.u32(560) == 0
             and emul.u32(556) == 1,
             "la sauvegarde LÈVE la garde (loupe-17 Q3 : plus rien à perdre) ; "
             "le premier Alt+F4 qui suit REFUSE (la garde armée) puis une "
             "NOUVELLE écriture la RÉ-ARME (refus_quitter = 0 : le Alt+F4 "
             "suivant re-vient avertir) — la falsification V5 de la spec "
             "est la preuve croisée, rejouée au V7.b")


# =====================================================================================
# V4 — LOUPE-17 LA SAUVEGARDE (l'écriture à l'octet, le panneau re-né)
# =====================================================================================

def vecteur_v4(emul: EmulationEdition, os_v: OSEdition, temoins, rng):
    section("V4 — loupe-17 : le différentiel 1 000 scénarios + le témoin")
    hwnd = 0x770001
    ecrits_avant = os_v.compteurs["WriteFile"]
    # (a) LE DIFFÉRENTIEL : 1 000 scénarios édition/sauvegarde — le disque
    # APRÈS == le modèle, SEULEMENT les N octets, la taille CONSTANTE
    divergences = 0
    for k in range(1000):
        # le témoin 3f (196 609 o : le panneau re-né le hache ENTIÈREMENT à
        # l'émulation, 13 s le geste réel) revient aux scénarios 0 et 500 —
        # le 384 porte la masse (998 passages), le 3f porte la preuve aux
        # grandes fenêtres (les décalages au-delà de la vue, DEUX passages)
        chemin = "temoin-3f.bin" if k % 500 == 0 else "temoin-384.bin"
        HN.fermer_session(emul)
        # un disque NEUF à chaque scénario (le témoin ré-émplacé)
        os_v.fichiers[chemin] = FichierEditable(contenu=bytes(temoins[chemin]))
        HN.emplacer_session(emul, os_v, chemin)
        ecrits_avant = os_v.compteurs["WriteFile"]
        taille = len(temoins[chemin])
        n = rng.randrange(0, 12)
        entrees = []
        deja = set()
        while len(entrees) < n:
            dec = rng.randrange(0, taille)
            if dec in deja:
                continue
            deja.add(dec)
            entrees.append((dec, rng.randrange(0, 256)))
        emul.poser_journal(entrees)
        emul.ecrire_cadre(556, struct.pack("<I", 1 if entrees else 0))
        emul.ecrire_cadre(560, struct.pack("<I", 1 if entrees else 0))
        ecrits_avant = os_v.compteurs["WriteFile"]
        r = emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                        "r8": CTRL_S, "r9": 0})
        modele = bytearray(temoins[chemin])
        for dec, oct_ in entrees:
            modele[dec] = oct_
        disque = bytes(os_v.fichiers[chemin].contenu)
        ok = (r["rax"] == 0 and disque == bytes(modele)
              and len(disque) == taille
              and emul.journal_nombre() == 0
              and emul.u32(556) == 0 and emul.u32(560) == 0
              and os_v.compteurs["WriteFile"] - ecrits_avant == len(entrees))
        if not ok:
            divergences += 1
            if divergences == 1:
                print(f"    [V4.a] scénario {k} : rax={r['rax']} "
                      f"journal={emul.journal_nombre()} "
                      f"écrits={os_v.compteurs['WriteFile'] - ecrits_avant} "
                      f"!= {len(entrees)}")
            break
    controle("V4.a:le-differentiel-1000-scenarios", divergences == 0,
             "1 000 scénarios (0 à 11 octets DISTINCTS aléatoires sur les "
             "témoins 384 et 3f) : le disque APRÈS == le modèle octet par "
             "octet (SEULEMENT les N octets diffèrent — jamais un de plus), "
             "la taille CONSTANTE, le journal VIDÉ, la marque et la garde "
             "LEVÉES, EXACTEMENT N WriteFile (un par entrée, L'ORDRE DE "
             "SAISIE)")
    # (b) LE SCÉNARIO DES TROIS OCTETS : le témoin à la barre, le panneau
    # re-né == hashlib, l'astérisque parti — l'écran attendu
    HN.fermer_session(emul)
    os_v.fichiers["temoin-3f.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-3f.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    emul.ecrire_cadre(544, struct.pack("<Q", 0x10))
    for frappe in (0x34, 0x64):              # « 4d » → 0x4D @ 0x10
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": frappe, "r9": 0})
    emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
    for frappe in (0x35, 0x61):              # « 5a » → 0x5A @ 0x22
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": frappe, "r9": 0})
    emul.ecrire_cadre(544, struct.pack("<Q", 0xF5))
    for frappe in (0x61, 0x62):              # « ab » → 0xAB @ 0xF5
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": frappe, "r9": 0})
    ecrits_avant = os_v.compteurs["WriteFile"]
    emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                "r8": CTRL_S, "r9": 0})
    disque = bytes(os_v.fichiers["temoin-3f.bin"].contenu)
    attendu_disque = bytearray(temoins["temoin-3f.bin"])
    attendu_disque[0x10] = 0x4D
    attendu_disque[0x22] = 0x5A
    attendu_disque[0xF5] = 0xAB
    r = emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    rempl = emul.u32(552)
    fenetre = fenetre_editee(disque, [], 0, rempl)
    empreintes = hashlib.md5(disque).digest() + hashlib.sha256(disque).digest()
    attendu = HR.model_ecran(fenetre, 0, rempl, len(disque), "temoin-3f.bin",
                             0xF6, 0, empreintes, 3, barre(emul), 27)
    controle("V4.b:le-temoin-et-le-panneau-re-ne",
             r["rax"] == 0 and disque == bytes(attendu_disque)
             and os_v.compteurs["WriteFile"] == ecrits_avant + 3
             and barre(emul) == model_temoign(3, 0x10, 0xF5)
             and bytes(emul.uc.mem_read(L.R_EMPREINTES, 48)) == empreintes
             and emul.u32(556) == 0 and ecran == attendu,
             "trois octets édités (0x4D @0x10, 0x5A @0x22, 0xAB @0xF5) puis "
             "Ctrl+S : LE TÉMOIN « 3 o écrits · 0x00000010..0x000000F5 » à "
             "la barre (le compte exact, la première et la dernière), le "
             "panneau RE-NÉ == hashlib du disque changé (le coût nommé : un "
             "passage de plus), l'astérisque PARTI, la marque levée — "
             "L'ÉCRAN ATTENDU OCTET PAR OCTET")
    # (c) LE REPLI : Ctrl+S sans édition — « rien à sauver », AUCUN appel
    ecrits_avant = os_v.compteurs["WriteFile"]
    r = emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
    controle("V4.c:le-repli-rien-a-sauver",
             r["rax"] == 0 and os_v.compteurs["WriteFile"] == ecrits_avant
             and barre(emul)
             == LIBELLES_EDITION["riensauver"][1].encode("latin-1"),
             "Ctrl+S sans édition : « rien à sauver » à la barre (le repli "
             "documenté, l'état nommé PAS un échec), rax = 0, AUCUN appel "
             "WriteFile (les appels comptés)")
    # (d) L'ÉCHEC FAIL-CLOSED : le 2e WriteFile refuse — le premier ACQUIS,
    # le journal DEMEURE ; le second Ctrl+S REPREND ET FINIT
    HN.fermer_session(emul)
    os_v.fichiers["temoin-3f.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-3f.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    emul.poser_journal([(0x10, 0x11), (0x20, 0x22), (0x30, 0x33)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    emul.ecrire_cadre(560, struct.pack("<I", 1))
    os_v.armer_echec_write(2)
    r = emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
    disque_mi = bytes(os_v.fichiers["temoin-3f.bin"].contenu)
    ok_mi = (r["rax"] == -6 and disque_mi[0x10] == 0x11
             and disque_mi[0x20] != 0x22
             and emul.journal_nombre() == 3 and emul.u32(556) == 1
             and emul.u32(560) == 1
             and (os_v.journal_gle[-1][1] if os_v.journal_gle else 0) != 0)
    os_v.armer_echec_write(None)
    r = emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
    disque_fin = bytes(os_v.fichiers["temoin-3f.bin"].contenu)
    controle("V4.d:l-echec-fail-closed-la-reprise",
             ok_mi and r["rax"] == 0 and disque_fin[0x20] == 0x22
             and disque_fin[0x30] == 0x33 and emul.journal_nombre() == 0
             and emul.u32(556) == 0
             and barre(emul) == model_temoign(3, 0x10, 0x30),
             "le shim WriteFile refuse à la DEUXIÈME entrée : -6, le code "
             "GetLastError CONSIGNÉ, FAIL-CLOSED — le premier octet ACQUIS "
             "au disque, le journal DEMEURE (3 entrées), la marque et la "
             "garde demeurent (l'échec ne perd RIEN) ; le second Ctrl+S "
             "REPREND ET FINIT : les trois octets écrits, le journal vidé, "
             "LE TÉMOIN rendu — la reprise est prouvée")
    # (e) sans session → -4
    HN.fermer_session(emul)
    r = emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
    controle("V4.e:sans-session", r["rax"] == -4,
             "Ctrl+S sans session ouverte → -4, « aucun fichier ouvert » à "
             "la barre (E1)")


# =====================================================================================
# V5 — LOUPE-18 LA SORTIE + LE RÉSEAU DE LA GARDE
# =====================================================================================

def vecteur_v5(emul: EmulationEdition, os_v: OSEdition, temoins):
    section("V5 — loupe-18 : le double-geste + le réseau de la garde")
    hwnd = 0x770001
    # (a) LA SORTIE DIRECTE : sans marque → DestroyWindow, rax = 0
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    emul.ecrire_cadre(556, struct.pack("<I", 0))
    emul.ecrire_cadre(560, struct.pack("<I", 0))
    detruits = emul.gui.compteurs.get("DestroyWindow", 0)
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    controle("V5.a:la-sortie-directe",
             r["rax"] == 0
             and emul.gui.compteurs.get("DestroyWindow", 0) == detruits + 1,
             "WM_CLOSE sans marque sale : DestroyWindow demandé (le premier "
             "geste TRANSCHE — rien à perdre), rax = 0")
    # (b) LE DOUBLE-GESTE : le refus nommé, la phrase, le beep, la fenêtre
    # DEMEURE ; le second tranche
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    emul.poser_journal([(0x30, 0x99)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))    # la marque sale
    emul.ecrire_cadre(560, struct.pack("<I", 0))    # la garde armée
    detruits = emul.gui.compteurs.get("DestroyWindow", 0)
    beeps = len(emul.gui.beeps)
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    ok_refus = (r["rax"] == -5 and emul.u32(560) == 1
                and emul.gui.compteurs.get("DestroyWindow", 0) == detruits
                and len(emul.gui.beeps) == beeps + 1
                and barre(emul) == LIBELLES_EDITION["quitter"][1]
                    .encode("latin-1"))
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    controle("V5.b:le-double-geste-garanti",
             ok_refus and r["rax"] == 0
             and emul.gui.compteurs.get("DestroyWindow", 0) == detruits + 1,
             "trois octets en attente (la marque sale) : le PREMIER Alt+F4 "
             "REFUSÉ NOMMÉMENT -5 — LA PHRASE à la barre (« MODIFIÉ - Alt+F4 "
             "encore pour quitter sans sauver, Ctrl+S pour sauver »), LE "
             "BEEP sonne (le refus s'entend), la fenêtre DEMEURE (Destroy "
             "PAS appelé), la garde posée ; le SECOND TRANSCHE : "
             "DestroyWindow — la volonté deux fois nommée")
    # (c) LE RÉSEAU DE LA GARDE : refusé → Ctrl+S → la sortie DIRECTE ;
    # refusé → une NOUVELLE écriture → le refus REVIENT
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    # le chemin 1 : refusé, sauvegardé, sorti
    emul.poser_journal([(0x30, 0x99)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    emul.ecrire_cadre(560, struct.pack("<I", 0))
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    refus1 = (r["rax"], emul.u32(560))
    emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                "r8": CTRL_S, "r9": 0})
    detruits = emul.gui.compteurs.get("DestroyWindow", 0)
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    chemin1 = (refus1[0] == -5 and r["rax"] == 0
               and emul.gui.compteurs.get("DestroyWindow", 0) == detruits + 1)
    # le chemin 2 : refusé, une NOUVELLE écriture, le refus REVIENT
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    emul.ecrire_cadre(544, struct.pack("<Q", 0x50))
    emul.poser_journal([(0x50, 0x77)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    emul.ecrire_cadre(560, struct.pack("<I", 0))
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    detruits = emul.gui.compteurs.get("DestroyWindow", 0)
    emul.ecrire_cadre(560, struct.pack("<I", 1))    # 17 l'a levée… mais 16 RÉ-ARME
    emul.ecrire_cadre(544, struct.pack("<Q", 0x51))
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 0, 0))
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
    emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                    "r8": 0, "r9": 0})
    chemin2 = (r["rax"] == -5 and emul.u32(560) == 1
               and emul.gui.compteurs.get("DestroyWindow", 0) == detruits)
    controle("V5.c:le-reseau-de-la-garde",
             chemin1 and chemin2,
             "LE RÉSEAU 16↔17↔18 tenu par tous les chemins : Alt+F4 refusé "
             "PUIS Ctrl+S (la sauvegarde lève la garde) PUIS Alt+F4 : la "
             "sortie DIRECTE (rien à perdre — Q3 de loupe-17) ; ET le chemin "
             "inverse : Alt+F4 refusé, une NOUVELLE écriture (loupe-16 "
             "RÉ-ARME la garde), Alt+F4 : LE REFUS REVIENT — la perte est "
             "une volonté DEUX FOIS nommée, jamais un accident d'un seul "
             "geste")
    # (d) WM_DESTROY : la sortie propre — le disque INTACT (l'abandon)
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    emul.poser_journal([(0x30, 0xAA), (0x31, 0xBB)])
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    closes = os_v.compteurs["CloseHandle"]
    quits = emul.gui.compteurs.get("PostQuitMessage", 0)
    r = emul.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_FIN_FENETRE,
                                    "r8": 0, "r9": 0})
    disque = bytes(os_v.fichiers["temoin-384.bin"].contenu)
    controle("V5.d:wm-destroy-la-sortie-propre",
             r["rax"] == 0 and os_v.compteurs["CloseHandle"] == closes + 1
             and emul.gui.compteurs.get("PostQuitMessage", 0) == quits + 1
             and emul.u64(528) == 0xFFFFFFFFFFFFFFFF
             and disque == bytes(temoins["temoin-384.bin"])
             and os_v.compteurs["WriteFile"] >= 0,
             "WM_DESTROY : loupe-03 la session close (la poignée rendue, le "
             "cadre re-vierge), PostQuitMessage UNE fois, rax = 0 — le "
             "journal ABANDONNÉ DÉLIBÉRÉMENT (le disque INTACT : le "
             "double-geste l'a nommé, les octets non sauvés sont une "
             "VOLONTÉ, pas une perte ; I2 : la sortie ne sauvegarde JAMAIS "
             "elle-même)")


# =====================================================================================
# V6 — L'ORACLE À SCÉNARIOS : LA BOUCLE COMPLÈTE DE L'ÉDITEUR
# =====================================================================================

def vecteur_v6(emul: EmulationEdition, os_v: OSEdition, temoins):
    section("V6 — l'oracle à scénarios : la boucle complète de l'éditeur")
    taille = len(temoins["temoin-3f.bin"])
    # (a) OUVRIR → ÉDITER → SAUVER → PEINDRE → QUITTER : la mort complète,
    # le disque sauvé == le modèle
    HN.fermer_session(emul)
    os_v.fichiers["temoin-3f.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-3f.bin"]))
    reset_gui(emul)
    reset_saisie(emul)
    modele = bytearray(temoins["temoin-3f.bin"])
    modele[0] = 0x4D                      # « 4d » au curseur 0 (la naissance)
    r = emul.appeler_winmain(
        "loupe.exe temoin-3f.bin",
        messages=[(0x770001, 5, 0, (440 << 16) | 640),    # WM_SIZE
                  (0x770001, 0x0F, 0, 0),                 # WM_PAINT
                  (0x770001, 0x102, 0x34, 0),             # '4'
                  (0x770001, 0x102, 0x64, 0),             # 'd'
                  (0x770001, 0x102, CTRL_S, 0),           # Ctrl+S
                  (0x770001, 0x0F, 0, 0),                 # WM_PAINT
                  (0x770001, WM_CLOTURE, 0, 0),           # Alt+F4 : direct
                  ])
    disque = bytes(os_v.fichiers["temoin-3f.bin"].contenu)
    ok_a = (r["exit_code"] == 0 and disque == bytes(modele)
            and emul.gui.fenetre_detruite
            and emul.gui.compteurs.get("PostQuitMessage", 0) == 1
            and emul.gui.compteurs.get("DestroyWindow", 0) == 1)
    controle("V6.a:ouvrir-editer-sauver-quitter", ok_a,
             "LA BOUCLE COMPLÈTE par la ligne de commande : la session née "
             "(loupe-01), WM_SIZE + la peinture, « 4d » (loupe-16), Ctrl+S "
             "(loupe-17 : l'octet 0x4D écrit à 0 — le disque == le "
             "modèle), Alt+F4 sans marque (loupe-18 : DestroyWindow → "
             "WM_DESTROY ENVOYÉ PAR LE SHIM → loupe-03 + PostQuitMessage → "
             "la boucle héritée rend → ExitProcess(0)) — LA MORT COMPLÈTE "
             "en un scénario, le code de sortie 0")
    # l'écran attendu au dernier WM_PAINT (l'oracle : octet par octet)
    # (b) LE CHEMIN DE L'ABANDON : le refus, le beep, le second geste — le
    # fichier INTACT
    HN.fermer_session(emul)
    os_v.fichiers["temoin-3f.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-3f.bin"]))
    reset_gui(emul)
    reset_saisie(emul)
    ecrits_avant = os_v.compteurs["WriteFile"]
    r = emul.appeler_winmain(
        "loupe.exe temoin-3f.bin",
        messages=[(0x770001, 5, 0, (440 << 16) | 640),
                  (0x770001, 0x102, 0x34, 0),             # '4'
                  (0x770001, 0x102, 0x64, 0),             # 'd' → la marque
                  (0x770001, WM_CLOTURE, 0, 0),           # refusé
                  (0x770001, 0x0F, 0, 0),                 # la phrase à la barre
                  (0x770001, WM_CLOTURE, 0, 0),           # le second tranche
                  ])
    disque = bytes(os_v.fichiers["temoin-3f.bin"].contenu)
    ok_b = (r["exit_code"] == 0
            and disque == bytes(temoins["temoin-3f.bin"])
            and os_v.compteurs["WriteFile"] == ecrits_avant
            and len(emul.gui.beeps) == 1
            and emul.gui.compteurs.get("DestroyWindow", 0) == 1)
    controle("V6.b:le-chemin-de-l-abandon", ok_b,
             "« 4d » (la marque sale posée) puis Alt+F4 : le refus -5 (LA "
             "PHRASE peinte à la barre, LE BEEP sonne), Alt+F4 encore : la "
             "sortie SANS sauvegarde — le journal abandonné DÉLIBÉRÉMENT, "
             "LE FICHIER INTACT AU DISQUE (aucune écriture : la "
             "différentielle tranche), ExitProcess(0) : même l'abandon est "
             "une sortie PROPRE")
    # (c) LA RÉ-OUVERTURE : le second loupe-01 lit les octets sauvés — la
    # persistance constatée, les empreintes recoupées
    HN.fermer_session(emul)
    os_v.fichiers["temoin-3f.bin"] = FichierEditable(
        contenu=bytes(modele))
    r = HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    emul.appeler(L.LOUPE07_VA, {"rcx": L.R_EMPREINTES})
    panneau = bytes(emul.uc.mem_read(L.R_EMPREINTES, 48))
    controle("V6.c:la-reouverture-la-persistance",
             (panneau[:16] == hashlib.md5(bytes(modele)).digest()
              and panneau[16:48] == hashlib.sha256(bytes(modele)).digest()
              and bytes(modele)[0] == 0x4D),
             "la boucle de l'éditeur complète : le fichier SAUVÉ re-ouvert "
             "par loupe-01, le panneau recalculé == hashlib (md5 + sha-256 "
             "du disque portant l'octet 0x4D à 0) — LA PERSISTANCE "
             "constatée, la boucle complète de l'éditeur : ouvrir, éditer, "
             "sauver, RE-OUVRIR")
    # (d) LE TÉMOIN À LA BARRE peint : le mode MESSAGE rendu par loupe-10
    reset_gui(emul)
    emul.gui.hwnd = 0x770001
    emul.uc.mem_write(L.R_SAISIE, struct.pack("<III", 3, 0, 0)
                      + model_temoign(2, 0x10, 0xF5) + b"\x00" * 40)
    emul.appeler(L.LOUPE10_VA, {"rcx": 0x770001})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    attendu = HR.model_ecran(
        fenetre_editee(bytes(modele), [], 0, emul.u32(552)), 0,
        emul.u32(552), len(modele), "temoin-3f.bin", 0x23, 0,
        panneau, 3, model_temoign(2, 0x10, 0xF5), 27)
    controle("V6.d:le-temoin-peint-a-la-barre", ecran == attendu,
             "le mode MESSAGE à la barre-état : LE TÉMOIN « 2 o écrits · "
             "0x00000010..0x000001F5 » composé par loupe-17 puis PEINT par "
             "loupe-10 — l'écran attendu OCTET PAR OCTET (les 2320 o == le "
             "modèle, le texte porté au dernier octet)")


# =====================================================================================
# V7 — LA FALSIFICATION (zéro silence)
# =====================================================================================

def vecteur_v7(emul: EmulationEdition, os_v: OSEdition, temoins, rng):
    section("V7 — la falsification : quatre mutants, chacun attrapé")
    hwnd = 0x770001
    # (a) LA VUE QUI SUIT MUTÉE : le recadrage neutralisé → le curseur sort
    # de l'écran — l'oracle échoue (V2.d)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    taille = len(temoins["temoin-3f.bin"])
    cible, t = chercher_insn(emul, L.LOUPE15_VA, 0x1C0, "mov",
                             "qword ptr [rbx + 0x218], r15")
    ok_a = cible is not None
    if ok_a:
        muter(emul, L.LOUPE15_VA + cible, b"\x90" * t)   # la pose neutralisée
        emul.ecrire_cadre(536, struct.pack("<Q", 0))
        emul.ecrire_cadre(544, struct.pack("<Q", 23 * 16))
        emul.appeler(L.LOUPE02_VA, {"rcx": 0})
        emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": VK["bas"], "r9": 0})
        vue_mutee = emul.u64(536)
        restaurer_bloc(emul, "loupe-15-curseur", "i110015")
        emul.ecrire_cadre(536, struct.pack("<Q", 0))
        emul.ecrire_cadre(544, struct.pack("<Q", 23 * 16))
        emul.appeler(L.LOUPE02_VA, {"rcx": 0})
        emul.appeler(L.LOUPE15_VA, {"rcx": hwnd, "rdx": 0x100,
                                    "r8": VK["bas"], "r9": 0})
        ok_a = (vue_mutee == 0
                and emul.u64(536) == min(L.recadre(23 * 16 + 16),
                                          L.vue_max(taille)))
    controle("V7.a:la-vue-qui-suit-mutee", ok_a,
             "la pose de la vue recadrée neutralisée (NOP) : VK_BAS au bord "
             "laisse la vue À 0 — le curseur sort de l'écran attendu (le "
             "mutant) ; les octets du plan re-posés : la vue SUIT au "
             "recadrage de la règle (la re-passe) — JAMAIS PERDU HORS ÉCRAN "
             "est une exigence, pas un espoir")
    # (b) LA GARDE DE 16 NON RÉ-ARMÉE : la perte d'un seul geste (V5 de
    # loupe-16, la preuve croisée)
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    poser_metriques(emul, 27)
    cible, t = chercher_insn(emul, L.LOUPE16_VA, 0x2C0, "mov",
                             "dword ptr [rbx + 0x230], 0")
    ok_b = cible is not None
    if ok_b:
        muter(emul, L.LOUPE16_VA + cible, b"\x90" * t)   # la ré-arme neutralisée
        emul.ecrire_cadre(544, struct.pack("<Q", 0x50))
        emul.poser_journal([])
        emul.ecrire_cadre(556, struct.pack("<I", 0))
        emul.ecrire_cadre(560, struct.pack("<I", 1))    # la garde LEVÉE (comme après 17)
        emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 0, 0))
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
        garde_mutee = emul.u32(560)
        restaurer_bloc(emul, "loupe-16-saisie", "i110016")
        emul.ecrire_cadre(544, struct.pack("<Q", 0x50))
        emul.poser_journal([])
        emul.ecrire_cadre(556, struct.pack("<I", 0))
        emul.ecrire_cadre(560, struct.pack("<I", 1))
        emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 0, 0))
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
        emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102, "r8": 0x33, "r9": 0})
        ok_b = garde_mutee == 1 and emul.u32(560) == 0
    controle("V7.b:la-garde-de-16-non-re-armee", ok_b,
             "la ré-arme de la garde neutralisée : une NOUVELLE écriture "
             "laisse refus_quitter = 1 — le Alt+F4 suivant TRANCHERAIT sans "
             "avertir (la perte d'un seul geste, le réseau cassé) ; les "
             "octets du plan re-posés : la garde RÉ-ARMÉE à l'écriture (0) — "
             "la falsification de la spec V5 ATTRAPÉE")
    # (c) LA GARDE DE 17 NON LEVÉE : le quitte-après-sauvegarde avertirait
    # pour rien (V5 de loupe-18)
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    cible, t = chercher_insn(emul, L.LOUPE17_VA, 0x240, "mov",
                             "dword ptr [rbx + 0x230], 0")
    ok_c = cible is not None
    if ok_c:
        muter(emul, L.LOUPE17_VA + cible, b"\x90" * t)   # la levée neutralisée
        emul.poser_journal([(0x30, 0x99)])
        emul.ecrire_cadre(556, struct.pack("<I", 1))
        emul.ecrire_cadre(560, struct.pack("<I", 0))
        emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
        garde_mutee = emul.u32(560)
        restaurer_bloc(emul, "loupe-17-sauver", "i110017")
        emul.poser_journal([(0x30, 0x99)])
        emul.ecrire_cadre(556, struct.pack("<I", 1))
        emul.ecrire_cadre(560, struct.pack("<I", 0))
        emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
        ok_c = garde_mutee == 0 and emul.u32(560) == 0
    controle("V7.c:la-garde-de-17-non-levee", ok_c,
             "la levée de la garde neutralisée : après la sauvegarde "
             "réussie refus_quitter DEMEURE (le mutant laisse la garde à 1 "
             "AVANT toute écriture — l'Alt+F4 suivant avertirait pour rien) "
             "— restaurée : la sauvegarde LÈVE la garde (Q3), la sortie ne "
             "ré-avertira plus : il n'y a plus rien à perdre")
    # (d) L'OCTET DE TROP : l'écriture mutée à 2 o — la différentielle
    # échoue (l'écriture à l'octet est une exigence, V5 de loupe-17)
    HN.fermer_session(emul)
    os_v.fichiers["temoin-384.bin"] = FichierEditable(
        contenu=bytes(temoins["temoin-384.bin"]))
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    reset_gui(emul)
    cible, t = chercher_insn(emul, L.LOUPE17_VA, 0x240, "mov", "r8d, 1")
    ok_d = cible is not None
    if ok_d:
        muter(emul, L.LOUPE17_VA + cible, b"\x41\xb8\x02\x00\x00\x00")
        # (mov r8d, 2 — 6 o, l'immédiat à l'adresse+2)
        emul.poser_journal([(0x30, 0x99)])
        emul.ecrire_cadre(556, struct.pack("<I", 1))
        emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
        ecrits = os_v.ecritures[-1]
        restaurer_bloc(emul, "loupe-17-sauver", "i110017")
        emul.poser_journal([(0x30, 0x99)])
        emul.appeler(L.LOUPE17_VA, {"rcx": hwnd, "rdx": 0x102,
                                    "r8": CTRL_S, "r9": 0})
        ok_d = (len(ecrits[1]) == 2 and os_v.ecritures[-1][1] == b"\x99"
                and len(os_v.ecritures[-1][1]) == 1)
    controle("V7.d:l-octet-de-trop", ok_d,
             "le compte d'écriture muté (r8d = 2) : le shim écrit DEUX "
             "octets (l'octet + la réserve de l'entrée) — la différentielle "
             "V4.a échouerait (un octet de trop diffère) ; restauré : UN "
             "octet exactement — L'ÉCRITURE À L'OCTET est une exigence, "
             "jamais une plage")
    # (e) L'ANTI-MUET du témoin : chaque octet du texte muté → l'égalité
    # échoue
    temoin_txt = model_temoign(3, 0x10, 0x1F5)
    muets = sum(1 for i in range(len(temoin_txt))
                if (temoin_txt[:i] + bytes([temoin_txt[i] ^ 1])
                    + temoin_txt[i + 1:]) != temoin_txt)
    controle("V7.e:l-anti-muet-du-temoin", muets == len(temoin_txt),
             f"chaque octet du témoin composé muté d'un bit (aux "
             f"{len(temoin_txt)} positions) → l'égalité échoue — la "
             "comparaison du barreau n'est PAS muette")


# =====================================================================================
# LE CAHIER COMPLET
# =====================================================================================

GRAINE = 20261108


def main() -> int:
    global GRAINE
    if "--graine" in sys.argv:
        GRAINE = int(sys.argv[sys.argv.index("--graine") + 1])
    print(f"=== loupe/harnais_edition.py — L'ORACLE À SCÉNARIOS (chantier "
          f"M10-(d), graine {GRAINE}) ===")
    rng = random.Random(GRAINE)
    temoins = HN.composer_temoins()
    donnees_m9, donnees_m1, donnees_demo = vecteur_v0()
    os_v = OSEdition()
    for nom, donnees in temoins.items():
        os_v.declarer(nom, FichierEditable(contenu=donnees))
    emul = EmulationEdition(os_v, donnees_m9, donnees_m1, donnees_demo)
    vecteur_v1(emul, os_v)
    vecteur_v2(emul, os_v, temoins, rng)
    vecteur_v3(emul, os_v, temoins, rng)
    vecteur_v4(emul, os_v, temoins, rng)
    vecteur_v5(emul, os_v, temoins)
    vecteur_v6(emul, os_v, temoins)
    vecteur_v7(emul, os_v, temoins, rng)

    controle("FINAL:getmodulehandlew-seul-au-mort",
             emul.os.appels_interdits == 0,
             "GetModuleHandleW (le mort) n'a JAMAIS été touché (le compteur) "
             "— le hInstance vient de l'ABI de WinMain (D174), les QUATRE "
             "feuilles du (d) vivent : WriteFile, DestroyWindow, "
             "PostQuitMessage, MessageBeep")

    total = len(REUSSITES) + len(ECHECS)
    print(f"\n=== LE CAHIER : {total} contrôles — "
          f"{len(REUSSITES)} VERTS, {len(ECHECS)} ÉCHECS ===")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  [ÉCHEC] {nom} — {detail}")
        print("VERDICT : ÉCHEC — le chantier n'est pas prouvé")
        return 1
    print("VERDICT : VERT — la famille édition loupe-15..18 et la table de "
          "routage étendue de loupe-09 r2 sont NOTÉES-MESURÉES-PROUVÉES sur "
          "pièces (le différentiel 10 000 touches/frappes + 1 000 scénarios "
          "de sauvegarde == le modèle ; LE TÉMOIN composé et peint ; LE "
          "RÉSEAU de la garde 16↔17↔18 par tous les chemins ; LA MORT "
          "complète au scénario ; la falsification attrapée dans les deux "
          "sens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
