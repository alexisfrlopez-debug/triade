#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite16_d210.py — L'ORACLE DU BLOC AU PÉRIMÈTRE LIVRÉ, l'unité
04 D210 (loupe-16 saisie × bras T — le juge = le modèle indépendant).

LES VECTEURS DEPUIS LE CONTRAT (loupe/I/loupe-16-saisie.md — l'oracle
dérivé de I, écrit-avant-code : oracle-depuis-I.txt) : le harnais du
domaine à l'édition (harnais_edition.EmulationEdition : les 18 blocs,
les feuilles IAT VIVANTES, le disque saisissable) porte LA NOTATION DE
CAMPAGNE au slot loupe-16 (0x6240) — le premier bloc de campagne À
ÉTAT : le journal, le tampon, la marque, la garde, la vue qui suit (le
renvoi de loupe-15 Q3, LOUPE02 la relit, la feuille repeint).

  V1 (le différentiel) : 10 000 frappes (hexa des deux casses, ~2 %
      VK_SUPPR, ~2 % non-hexa ; DEUX disques : le témoin 63 o ET le grand
      8 192 o — la vue suit, les relectures LOUPE02, le recouvrement du
      journal, LA FRONTIÈRE des 256 distincts) : journal + tampon +
      attente + curseur + vue + remplissage + marque + garde == le modèle
      Python à CHAQUE frappe, l'état propre (les non-volatils rendus —
      rsi/rdi JAMAIS touchés par la composition de campagne, la pile
      équilibrée, les canaris intacts), les compteurs exacts (ReadFile
      ne bouge que pour suivre, InvalidateRect à chaque écriture) ;
  V2 (le scénario doré) : « 4d5a » au curseur 0x22 — le journal [(0x22,
      0x4D), (0x23, 0x5A)], la marque, la garde ré-armée, la cellule
      suivante active, L'ÉCRAN attendu (loupe-10, les 2320 o == le
      modèle) ; ET LA VUE QUI SUIT au grand disque (le curseur au bord
      de la vitrine → le recadrage, la relecture, le recouvrement) ;
  V3 (les rejets) : E1 sans session → -4 nommé ; E2 la cellule fantôme
      → -3, RIEN au journal, l'attente CONSOMMÉE — ET la fantôme MARCHE
      SALE (remplissage u32 : le refus tient même après une écriture) ;
      le fichier vide → -3 ; E3 le 257e distinct → -3 « journal plein -
      Ctrl+S », RIEN perdu ;
  V4 (le repli) : « z », « ! », l'espace IGNORÉS (rax = 0, rien) ;
      VK_SUPPR à l'attente : le nibble effacé ; hors attente : ignoré ;
  V5 (la falsification demandée) : la garde NON ré-armée à l'écriture
      (le mutant : les DEUX NOP à la place du « mov [rbx+560], 0 ») —
      le scénario de loupe-18 (éditer PUIS Alt+F4 UNE SEULE fois doit
      AVERTIR) ÉCHOUE au mutant (la fenêtre meurt, jamais le refus -5)
      — la falsification TRAVERSE LES BLOCS, l'oracle à scénarios
      l'attrape ; la notation juste re-jouée VERTE.

Usage : python3 scripts/campagne_d204/unite-16-T-d210/oracle_unite16_d210.py
Sortie : 0 = oracle VERT (falsification comprise) ; 2 = refus nommé.
"""
from __future__ import annotations

import hashlib
import os
import random
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-16-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import harnais_rendu as HR          # noqa: E402  (l'écran attendu)
import harnais_edition as HE        # noqa: E402  (le disque saisissable)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

import importlib.util as _ilu       # noqa: E402  (l'auteur, pour le mutant)
_sys_layout = sys.modules.get("layout")
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L_layout = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L_layout
_spec_l.loader.exec_module(L_layout)
_spec_a = _ilu.spec_from_file_location(
    "auteur_oracle16", os.path.join(REPO, "loupe", "outils", "auteur.py"))
AUTEUR = _ilu.module_from_spec(_spec_a)
sys.modules["auteur_oracle16"] = AUTEUR
_spec_a.loader.exec_module(AUTEUR)
if _sys_layout is not None:
    sys.modules["layout"] = _sys_layout   # le monde tel qu'il était
else:
    del sys.modules["layout"]

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(UNITE, "notation", "loupe-16-saisie.asm")
GRAINE = 20261115                    # la graine fixe des tirages (T == terrain)
WM_CLOTURE = HE.WM_CLOTURE if hasattr(HE, "WM_CLOTURE") else 0x10

VERTS, ROUGES = 0, 0


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def refus(nom: str, detail: str) -> None:
    print(f"[oracle-unite16-d210] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


# ==================== LE MODÈLE INDÉPENDANT (jamais les octets du bloc) =====


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


def m_lignes_visibles(lignes: int) -> int:
    return min(24, max(0, lignes - 3))


def m_vue_suit(curseur: int, vue: int, taille: int, lignes: int):
    """LA VUE SUIT (le renvoi de loupe-15 Q3) : la vitrine [vue, vue+16·V)."""
    v = m_lignes_visibles(lignes)
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min(L.recadre(curseur), L.vue_max(taille))
    return (nv, nv != vue)


def fenetre_editee(disk: bytes, journal: list, vue: int, remplissage: int):
    """Les octets du DISQUE + LE RECOUVREMENT du journal (loupe-02 Q2)."""
    fen = bytearray(disk[vue:vue + remplissage])
    for dec, oct_ in journal:
        if vue <= dec < vue + remplissage:
            fen[dec - vue] = oct_
    return bytes(fen)


def m_curseur_apres(curseur: int, taille: int) -> int:
    return min(curseur + 1, taille - 1) if taille > 1 else 0


class EmulationCampagne(HE.EmulationEdition):
    """Le harnais du domaine au slot loupe-16 PORTANT LA PIÈCE DE CAMPAGNE :
    les dix-sept autres blocs demeurent les notations scellées (la saisie
    appelle loupe-02 le scellé et la feuille InvalidateRect — les deux
    vivants au harnais)."""

    def __init__(self, os_virtuel, notation=NOTATION, verifier_piece=True):
        m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
        m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
        demo = open(os.path.join(HN.TRIADE, HR.SCELLE_DEMO), "rb").read()
        if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
                or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
            refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
        super().__init__(os_virtuel, m9, m1, demo)
        rva, slot = L.SLOTS_LOUPE["i110016"]
        if not os.path.exists(notation):
            refus("NOTATION-ABSENTE", f"{notation} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, notation, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110016"] = (octets, metas)
        if not verifier_piece:
            return
        # LA PIÈCE LIVRÉE porte les MÊMES octets au slot (le juge éprouve
        # ce qui part au coffre, jamais une copie privée)
        piece = os.path.join(UNITE, "piece", "loupe.exe")
        if not os.path.exists(piece):
            refus("PIÈCE-ABSENTE", f"{piece} — construire d'abord")
        brut = open(piece, "rb").read()
        e = struct.unpack_from("<I", brut, 0x3C)[0]
        nb = struct.unpack_from("<H", brut, e + 6)[0]
        opt = struct.unpack_from("<H", brut, e + 20)[0]
        posee = None
        for k in range(nb):
            o = e + 24 + opt + k * 40
            va = struct.unpack_from("<I", brut, o + 12)[0]
            vs = struct.unpack_from("<I", brut, o + 8)[0]
            ra = struct.unpack_from("<I", brut, o + 20)[0]
            if va <= rva < va + vs:
                posee = brut[ra + rva - va:ra + rva - va + slot]
        if posee is None or posee[:len(octets)] != octets \
                or posee[len(octets):] != b"\x90" * (slot - len(octets)):
            refus("SLOT-HORS-PIÈCE",
                  "le slot loupe-16 de la pièce ne porte pas la notation "
                  "de campagne + le padding NOP — la pièce est fausse")


def frapper(emul, hwnd: int, ch: int):
    return emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                       "r8": ch, "r9": 0})


def poser_etat(emul, curseur: int, vue: int = 0):
    emul.ecrire_cadre(536, struct.pack("<Q", vue))
    emul.ecrire_cadre(544, struct.pack("<Q", curseur))


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 04 D210 (loupe-16 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    rng = random.Random(GRAINE)
    temoins = HN.composer_temoins()
    grand = bytes((i * 31 + 7) & 0xFF for i in range(8192))
    os_v = HE.OSEdition()
    for nom, donnees in temoins.items():
        os_v.declarer(nom, HE.FichierEditable(contenu=donnees))
    os_v.declarer("grand-8k.bin", HE.FichierEditable(contenu=grand))
    os_v.declarer("temoin-vide.bin", HE.FichierEditable(contenu=b""))
    emul = EmulationCampagne(os_v)
    hwnd = 0x770001
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "

    # ---- V1 : LE DIFFÉRENTIEL — 10 000 frappes aux DEUX disques -------------
    print("\n-- V1 : le différentiel (10 000 frappes, le modèle indépendant) --")
    divergences = 0
    for nom_disque, disk, depart in (("temoin-3f.bin",
                                      temoins["temoin-3f.bin"], 0x22),
                                     ("grand-8k.bin", grand, 0x17E)):
        taille = len(disk)
        HN.fermer_session(emul)
        HN.emplacer_session(emul, os_v, nom_disque)
        HE.reset_gui(emul)
        HE.poser_metriques(emul, 27)
        HE.reset_saisie(emul)
        emul.poser_journal([])
        emul.ecrire_cadre(556, struct.pack("<I", 0))
        emul.ecrire_cadre(560, struct.pack("<I", 0))
        poser_etat(emul, depart, 0)
        journal: list = []
        modele_tampon = bytearray(disk[:384])
        curseur, vue, rempl = depart, 0, min(384, taille)
        m_actif, m_nibble = 0, 0
        lectures0 = os_v.compteurs["ReadFile"]
        repeints0 = emul.gui.compteurs.get("InvalidateRect", 0)
        lectures, repeints = 0, 0
        for _ in range(10_000):
            tirage = rng.random()
            if tirage < 0.02:
                frappe = 0x08
            elif tirage < 0.04:
                frappe = rng.choice(bruit)
            else:
                frappe = rng.choice(hexa)
            r = frapper(emul, hwnd, frappe)
            # — le modèle (jamais les octets du bloc) —
            if frappe == 0x08:
                if m_actif:
                    m_actif = 0
            elif chr(frappe) in "0123456789abcdefABCDEF":
                valeur = int(chr(frappe), 16)
                if not m_actif:
                    m_actif, m_nibble = 1, valeur
                else:
                    m_actif = 0
                    octet = (m_nibble << 4) | valeur
                    journal, refuse = m_journal_seconde(journal, curseur, octet)
                    if not refuse:
                        if vue <= curseur < vue + rempl:
                            modele_tampon[curseur - vue] = octet
                        curseur = m_curseur_apres(curseur, taille)
                        nv, relu = m_vue_suit(curseur, vue, taille, 27)
                        if relu:
                            lectures += 1
                            vue = nv
                            rempl = min(384, taille - vue)
                            modele_tampon = bytearray(
                                fenetre_editee(disk, journal, vue, rempl))
                        repeints += 1
            # — la comparaison (l'état lu, jamais le modèle) —
            probleme = None
            if r["rax"] not in (0, -3):
                probleme = f"le verdict {r['rax']} inattendu"
            elif not emul.etat_propre(r):
                probleme = "l'état impropre (non-volatils/pile/canaris)"
            actif, nibble = struct.unpack(
                "<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
            if probleme is None and (actif, nibble) != (
                    m_actif, m_nibble if m_actif else 0):
                probleme = f"l'attente ({actif},{nibble}) diverge"
            elif probleme is None and HE.lire_journal(emul) != journal:
                probleme = "le journal diverge"
            elif probleme is None and (emul.u64(544) != curseur
                                       or emul.u64(536) != vue):
                probleme = (f"curseur {emul.u64(544)} != {curseur} ou vue "
                            f"{emul.u64(536)} != {vue}")
            elif probleme is None and emul.u32(552) != rempl:
                probleme = f"remplissage {emul.u32(552)} != {rempl}"
            elif probleme is None and bytes(
                    emul.uc.mem_read(L.R_CADRE + 568, 384)) != bytes(modele_tampon):
                probleme = "le tampon diverge"
            elif probleme is None and emul.u32(556) != (1 if journal else 0):
                probleme = "la marque diverge"
            elif probleme is None and emul.u32(560) != 0:
                probleme = "la garde diverge"
            if probleme:
                divergences += 1
                if divergences <= 3:
                    print(f"    [{nom_disque}] {probleme}")
        ok_cpt = (os_v.compteurs["ReadFile"] - lectures0 == lectures
                  and emul.gui.compteurs.get("InvalidateRect", 0) - repeints0
                  == repeints)
        controle(f"V1:le-differentiel-10000-frappes-{nom_disque}",
                 divergences == 0,
                 f"le journal PAR DÉCALAGE (la réécriture REMPLACE, la borne "
                 "256 refusée), l'attente CONSOMMÉE, le tampon (le "
                 "recouvrement immédiat), la marque, LA GARDE RÉ-ARMÉE, le pas "
                 "clampé, LA VUE QUI SUIT — tout == le modèle, l'état propre "
                 "(rsi/rdi jamais touchés), les compteurs exacts")
        controle(f"V1:les-compteurs-exacts-{nom_disque}", ok_cpt,
                 f"ReadFile {lectures} relectures == la vue qui suit seule ; "
                 f"InvalidateRect {repeints} == les écritures seules")
        divergences = 0

    # ---- V2 : LE SCÉNARIO DORÉ — « 4d5a » + la vue qui suit ----------------
    print("\n-- V2 : le scénario doré (« 4d5a », l'écran attendu) --")
    temoin = temoins["temoin-3f.bin"]
    taille = len(temoin)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    HE.reset_gui(emul)
    HE.poser_metriques(emul, 27)
    HE.reset_saisie(emul)
    poser_etat(emul, 0x22, 0)
    for ch in (0x34, 0x64, 0x35, 0x61):          # 4 d 5 a
        frapper(emul, hwnd, ch)
    r = emul.appeler(L.LOUPE10_VA, {"rcx": hwnd})
    ecran = bytes(emul.uc.mem_read(L.R_ECRAN, 2320))
    rempl = emul.u32(552)
    attendu = HR.model_ecran(
        fenetre_editee(temoin, [(0x22, 0x4D), (0x23, 0x5A)], 0, rempl),
        0, rempl, taille, "temoin-3f.bin", 0x24, 1,
        bytes(emul.uc.mem_read(L.R_EMPREINTES, 48)), 0, b"", 27)
    controle("V2:le-scenario-4d5a-l-ecran-attendu",
             r["rax"] == 0 and emul.u64(544) == 0x24 and emul.u32(556) == 1
             and emul.u32(560) == 0
             and HE.lire_journal(emul) == [(0x22, 0x4D), (0x23, 0x5A)]
             and ecran == attendu,
             "« 4d5a » au curseur 0x22 : les DEUX octets au journal ET au "
             "tampon (visibles immédiatement), la marque sale, LA GARDE "
             "ré-armée, la cellule suivante active (curseur 0x24) — "
             "L'ÉCRAN ATTENDU octet par octet (les 2320 o == le modèle)")
    # la vue qui suit au grand disque : le curseur au bord → le recadrage
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "grand-8k.bin")
    HE.reset_gui(emul)
    HE.poser_metriques(emul, 27)
    HE.reset_saisie(emul)
    poser_etat(emul, 0x17E, 0)                    # 382 — la dernière cellule
    lectures0 = os_v.compteurs["ReadFile"]
    frapper(emul, hwnd, 0x34)
    r = frapper(emul, hwnd, 0x41)                 # « 4A » → l'octet 0x4A à 382 → 383
    controle("V2:la-vue-qui-suit-le-recadrage",
             r["rax"] == 0 and emul.u64(544) == 383 and emul.u64(536) == 0
             and os_v.compteurs["ReadFile"] == lectures0,
             "le curseur à 383 demeure DANS la vitrine [0, 384) : la vue "
             "IMMOBILE (aucune relecture), l'octet visible")
    frapper(emul, hwnd, 0x35)
    r = frapper(emul, hwnd, 0x30)                # l'octet 0x50 à 383 → 384
    attendu_tampon = fenetre_editee(grand, [(0x17E, 0x4A), (0x17F, 0x50)],
                                     208, 384)
    controle("V2:le-recadrage-et-la-relecture",
             r["rax"] == 0 and emul.u64(544) == 384 and emul.u64(536) == 208
             and os_v.compteurs["ReadFile"] == lectures0 + 1
             and bytes(emul.uc.mem_read(L.R_CADRE + 568, 384)) == attendu_tampon
             and emul.u32(552) == 384,
             "le curseur au-delà de la vitrine → la nouvelle vue "
             "aligne16_inf(384 − 176) = 208, LA RELECTURE LOUPE02 (une "
             "seule), le recouvrement du journal au tampon — la cellule "
             "suivante ATTEND à l'écran (l'invariant du domaine)")

    # ---- V3 : LES REJETS — E1, la fantôme (même sale), le vide, E3 ---------
    print("\n-- V3 : les rejets (E1/E2/E3, le vide) --")
    HN.fermer_session(emul)
    r = frapper(emul, hwnd, 0x34)
    controle("V3:E1-sans-session",
             r["rax"] == -4 and HE.barre(emul)
             == HR.LIBELLES["session"][1].encode("latin-1"),
             "sans session ouverte → -4, « aucun fichier ouvert » à la barre")
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    poser_etat(emul, 384 + 5, 0)
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    emul.poser_journal([])
    r = frapper(emul, hwnd, 0x64)
    actif, nibble = struct.unpack("<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
    controle("V3:E2-la-cellule-fantome",
             r["rax"] == -3 and emul.journal_nombre() == 0 and actif == 0
             and HE.barre(emul) == HR.LIBELLES["horsbornes"][1].encode("latin-1"),
             "le curseur forgé au-delà du remplissage → -3 « hors bornes », "
             "RIEN au journal (le refus PRÉCÈDE), l'attente CONSOMMÉE")
    # la fantôme MARCHE SALE : le remplissage lu u32 — le refus tient même
    # après une écriture (la composition de campagne ne lit JAMAIS le qword)
    emul.poser_journal([])
    poser_etat(emul, 384 + 5, 0)
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    emul.ecrire_cadre(556, struct.pack("<I", 1))
    r = frapper(emul, hwnd, 0x64)
    controle("V3:E2-la-fantome-marche-sale",
             r["rax"] == -3 and emul.journal_nombre() == 0,
             "la marque sale posée (une écriture vécue) : la fantôme "
             "REFUSÉE QUAND MÊME — le remplissage lu u32 SEUL (@+552, jamais "
             "le qword : la marque vit à +556)")
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-vide.bin")
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    poser_etat(emul, 0, 0)
    r = frapper(emul, hwnd, 0x64)
    controle("V3:le-fichier-vide", r["rax"] == -3 and emul.journal_nombre() == 0,
             "le fichier de taille zéro : aucune cellule n'existe → -3")
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-384.bin")
    poser_etat(emul, 0x20, 0)
    entrees = [(0x40 + i, (i * 7) & 0xFF) for i in range(256)]
    emul.poser_journal(entrees)
    emul.uc.mem_write(L.R_SAISIE + 4, struct.pack("<II", 1, 4))
    r = frapper(emul, hwnd, 0x64)
    controle("V3:E3-le-257e-distinct",
             r["rax"] == -3 and emul.journal_nombre() == 256
             and HE.lire_journal(emul) == entrees
             and HE.barre(emul) == HE.LIBELLES_EDITION["journalplein"][1]
                 .encode("latin-1"),
             "le 257e distinct → -3 « journal plein - Ctrl+S », les 256 "
             "premiers INTACTS (RIEN perdu)")

    # ---- V4 : LE REPLI — le non-hexa, VK_SUPPR -----------------------------
    print("\n-- V4 : le repli (le non-hexa, VK_SUPPR) --")
    emul.poser_journal([])
    emul.uc.mem_write(L.R_SAISIE, b"\x00" * 96)
    emul.ecrire_cadre(556, struct.pack("<I", 0))
    for ch in (0x7A, 0x21, 0x20):                  # z ! espace
        r = frapper(emul, hwnd, ch)
        if r["rax"] != 0 or emul.journal_nombre() != 0:
            break
    controle("V4:le-non-hexa-ignore",
             r["rax"] == 0 and emul.journal_nombre() == 0
             and emul.u32(556) == 0,
             "« z », « ! », l'espace IGNORÉS proprement (rax = 0, rien bougé)")
    HE.reset_saisie(emul)
    frapper(emul, hwnd, 0x34)
    frapper(emul, hwnd, 0x08)
    actif, nibble = struct.unpack("<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
    r = frapper(emul, hwnd, 0x08)
    controle("V4:vk-suppr-a-l-attente",
             actif == 0 and nibble == 0 and r["rax"] == 0
             and emul.journal_nombre() == 0,
             "« 4 » frappé (l'attente posée), VK_SUPPR : le nibble EFFACÉ "
             "(le premier chiffre repart) ; hors attente : ignoré")

    # ---- V5 : LA FALSIFICATION DEMANDÉE — la garde non ré-armée -------------
    print("\n-- V5 : la falsification (la garde non ré-armée) --")
    brouillon = open(os.path.join(UNITE, "brouillons", "loupe-16-saisie.asm"),
                     encoding="utf-8").read()
    cible = "mov dword ptr [rbx + 560], 0"
    if brouillon.count(cible) != 1:
        refus("MUTATION-INTROUVABLE",
              f"« {cible!r} » attendu UNE fois dans le brouillon")
    mutation = brouillon.replace(cible, "nop\nnop")
    dossier_brouillons_mut = os.path.join(UNITE, "epreuves", "brouillons-mut")
    dossier_notation_mut = os.path.join(UNITE, "epreuves")
    os.makedirs(dossier_brouillons_mut, exist_ok=True)
    with open(os.path.join(dossier_brouillons_mut, "falsifiee-garde.asm"),
              "w", encoding="utf-8") as f:
        f.write(mutation)
    AUTEUR.BROUILLONS = dossier_brouillons_mut
    AUTEUR.SORTIE = dossier_notation_mut
    AUTEUR.NOMS_COURTS["falsifiee-garde"] = (
        "la saisie : la garde non ré-armée (LE MUTANT de la falsification)")
    rva16, slot16 = L.SLOTS_LOUPE["i110016"]
    deps_mut = ("LE MUTANT de la falsification V5 : la garde de loupe-18 "
                "non ré-armée à l'écriture — le scénario Alt+F4 échoue")
    try:
        AUTEUR.resoudre_bloc(
            BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64), "falsifiee-garde",
            "i110016", "loupe-16:R1", rva16, slot16, deps_mut)
    except AUTEUR.ErreurAuteur as exc:
        refus("RÉSOLUTION-AUTEUR-MUTANT", str(exc))

    def scenario_garde(emul_x) -> tuple[int, int, bool]:
        """ÉDITER PUIS Alt+F4 UNE SEULE FOIS : (verdict, garde, l'averti)."""
        HN.fermer_session(emul_x)
        HN.emplacer_session(emul_x, os_v, "temoin-384.bin")
        HE.reset_gui(emul_x)
        HE.reset_saisie(emul_x)
        emul_x.poser_journal([])
        emul_x.ecrire_cadre(556, struct.pack("<I", 0))
        emul_x.ecrire_cadre(560, struct.pack("<I", 0))
        poser_etat(emul_x, 0x50, 0)
        # le premier Alt+F4 refusé (la garde armée) PUIS l'écriture
        emul_x.ecrire_cadre(560, struct.pack("<I", 1))
        frapper(emul_x, hwnd, 0x62)
        frapper(emul_x, hwnd, 0x62)                # « bb » → l'octet 0xBB
        garde_avant = emul_x.u32(560)
        beeps = len(emul_x.gui.beeps)
        r = emul_x.appeler(L.LOUPE18_VA, {"rcx": hwnd, "rdx": WM_CLOTURE,
                                          "r8": 0, "r9": 0})
        return r["rax"], garde_avant, (r["rax"] == -5
                                       and len(emul_x.gui.beeps) == beeps + 1)

    chemin_mut = os.path.join(dossier_notation_mut, "falsifiee-garde.asm")
    emul_mut = EmulationCampagne(HE.OSEdition(), notation=chemin_mut,
                                 verifier_piece=False)
    for nom, donnees in temoins.items():
        emul_mut.os.declarer(nom, HE.FichierEditable(contenu=donnees))
    v_juste, garde_juste, averti_juste = scenario_garde(emul)
    v_mut, garde_mut, averti_mut = scenario_garde(emul_mut)
    controle("V5:la-garde-re-armee-a-l-ecriture",
             garde_juste == 0 and averti_juste,
             "la notation juste : l'écriture ré-ARME la garde "
             "(refus_quitter = 0) — Alt+F4 UNE SEULE FOIS après l'édition "
             "AVERTIT (-5, le beep, la phrase) — le scénario de loupe-18 TIENT")
    controle("V5:le-mutant-attrape-par-le-scenario",
             garde_mut == 1 and not averti_mut and v_mut == 0,
             "le mutant (la garde non ré-armée) : Alt+F4 après l'édition "
             f"TRANCHE DIRECT (verdict {v_mut}, jamais le refus -5) — la "
             "falsification DEMANDÉE par le contrat, ATTRAPÉE par l'oracle "
             "à scénarios (la preuve traverse les blocs)")
    frapper(emul, hwnd, 0x62)
    r = frapper(emul, hwnd, 0x62)     # « bb » → l'écriture, la garde RÉ-ARMÉE
    controle("V5:la-notation-juste-re-jouee",
             r["rax"] == 0 and emul.u32(560) == 0 and emul.u32(556) == 1,
             "la notation de campagne re-devenue la même — le vert rendu "
             "au retrait de la mutation (l'écriture « bb » : la garde "
             "RÉ-ARMÉE à 0, la marque posée, rax = 0)")

    print(f"\n=== L'ORACLE {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
