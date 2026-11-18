#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_metriques_unite16.py — L'ÉPREUVE DES MÉTRIQUES (L5 — née du ROUGE
V1 du run terrain v3, l'Entrée 352) : LE JUGE POSE L'ÉCRAN QU'IL ANNONCE.

La faute nommée (la classe « les-metriques-ecran-jamais-posees-par-le-juge ») :
la pièce loupe-16 lit LES LIGNES VISIBLES à R_METRIQUES+8 [0xFDF8] (la zone que
le WM_SIZE de la vraie console remplit — layout.py : METRIQUES_LIGNES) ; le
harnais du labo la POSE (harnais_edition.poser_metriques(emul, 27) — l'oracle
l'appelle avant CHAQUE vecteur), l'épreuve POSIX la PASSE en argument (27) —
le scénario-juge né à la 349 (le premier terrain à état) n'a AUCUN geste pour
elle : la zone vit à SON ÉTAT STATIQUE dans l'exe — LES ZÉROS (constaté octet
par octet au .data : 0xFDF0..0xFE00 == 00). La pièce calcule donc
lignes_visibles = max(0, 0-3) = 0 → la vitrine = vue + 0×16 = LA VUE MÊME →
CHAQUE engagement au-delà du curseur 176 entre à .recadre (la vue rampe à
aligne16_inf(curseur-176), la relecture + le repeint à CHAQUE frappe) — pendant
que le modèle du juge tient la vitrine à 27-3 = 24 lignes = 384 : LA VUE
DIVERGE dès le premier recadrage de la pièce (l'engagement au curseur 191 → la
pièce pose la vue 16, le modèle la tient à 0).

L'épreuve (tenue au bac contre CHAQUE scénario livré à écran, AVEC l'épreuve
du guichet et l'épreuve de la liaison) :
  L5-a STRUCTURELLE — le scénario POSE la zone des métriques avant les
      vecteurs (l'écriture à 0xFDF0 présente au fichier) ;
  L5-b LE TERRAIN RECONSTITUÉ — le différentiel 10 000 frappes contre LA
      PIÈCE DE CAMPAGNE (le slot assemblé de la notation, la pièce livrée
      recoupée — EmulationCampagne), les métriques À LEUR ÉTAT STATIQUE (les
      zéros — l'état du terrain), le modèle du juge (lignes=27) : le ROUGE
      reconstitué, le problème IDENTIQUE MOT POUR MOT (« le curseur ou la vue
      divergent » == la console du terrain) ;
  L5-c LE LABO RECONSTITUÉ — les métriques POSÉES (27, le geste du harnais) :
      le MÊME différentiel VERT (0 divergence) — la pièce N'EST PAS en faute.

Usage : python3 scripts/campagne_d204/epreuve_metriques_unite16.py
"""

from __future__ import annotations

import os
import random
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-16-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import harnais_rendu as HR          # noqa: E402  (l'écran attendu — SCELLE_DEMO)
import harnais_edition as HE        # noqa: E402  (le disque saisissable)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

import importlib.util as _ilu       # noqa: E402
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L_layout = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L_layout
_spec_l.loader.exec_module(L_layout)
L = HN.L
B4 = HN.B4

GRAINE = 20261115                    # la graine fixe des tirages (T == terrain)
VK_SUPPR = 0x08
SCENARIO_V3 = os.path.join(UNITE, "kit", "kit-unite-04-d210-20261118-v3",
                           "scenario-unite16.py")

VERTS, ROUGES = 0, 0


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


# ---- LE MODÈLE DU JUGE (recopié VERBATIM du scénario livré — jamais réécrit)

def m_journal_seconde(journal: list, curseur: int, octet: int):
    for i, (dec, _) in enumerate(journal):
        if dec == curseur:
            journal[i] = (curseur, octet)
            return journal, False
    if len(journal) >= 256:
        return journal, True
    journal.append((curseur, octet))
    return journal, False


def m_vue_suit(curseur: int, vue: int, taille: int, lignes: int = 27):
    v = min(24, max(0, lignes - 3))
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min((max(0, curseur - 176)) & ~15,
             (max(0, taille - 384) + 15) & ~15 if taille > 384 else 0)
    return nv, nv != vue


def fenetre_editee(disk: bytes, journal: list, vue: int, remplissage: int):
    fen = bytearray(disk[vue:vue + remplissage])
    for dec, oct_ in journal:
        if vue <= dec < vue + remplissage:
            fen[dec - vue] = oct_
    return bytes(fen)


class EmulationCampagne(HE.EmulationEdition):
    """Le harnais du domaine au slot loupe-16 PORTANT LA PIÈCE DE CAMPAGNE
    (recopié de l'oracle — la pièce livrée recoupée au slot)."""

    def __init__(self, os_virtuel):
        m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
        m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
        demo = open(os.path.join(HN.TRIADE, HR.SCELLE_DEMO), "rb").read()
        super().__init__(os_virtuel, m9, m1, demo)
        rva, slot = L.SLOTS_LOUPE["i110016"]
        notation = os.path.join(UNITE, "notation", "loupe-16-saisie.asm")
        octets, metas = B4.assembler_bloc(self.ks, notation, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110016"] = (octets, metas)
        # la pièce LIVRÉE porte les MÊMES octets au slot (le juge éprouve ce
        # qui part au coffre)
        piece = os.path.join(UNITE, "kit", "kit-unite-04-d210-20261118-v3",
                             "loupe.exe")
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
            print("[REFUS] le slot loupe-16 de la pièce livrée != la notation")
            sys.exit(2)


def frapper(emul, hwnd: int, ch: int):
    return emul.appeler(L.LOUPE16_VA, {"rcx": hwnd, "rdx": 0x102,
                                       "r8": ch, "r9": 0})


def differential(emul, os_v, disk: bytes, pose_metriques: bool, arme: str):
    """Le V1 du scénario VERBATIM (la même graine, le même tirage, le même
    modèle lignes=27) — les métriques posées (le labo) ou à l'état statique
    (le terrain)."""
    taille = len(disk)
    HN.fermer_session(emul)
    HN.emplacer_session(emul, os_v, "temoin-3f.bin")
    HE.reset_gui(emul)
    HE.reset_saisie(emul)
    if pose_metriques:
        HE.poser_metriques(emul, 27)          # LE GESTE DU HARNAIS
    else:
        # L'ÉTAT DU TERRAIN : la zone à SON ÉTAT STATIQUE dans l'exe —
        # les zéros (constatés au .data du loupe.exe livré)
        emul.uc.mem_write(L.R_METRIQUES, b"\x00" * L.ZONE_METRIQUES)
    emul.poser_journal([])
    emul.ecrire_cadre(556, struct.pack("<I", 0))
    emul.ecrire_cadre(560, struct.pack("<I", 0))
    emul.ecrire_cadre(536, struct.pack("<Q", 0))
    emul.ecrire_cadre(544, struct.pack("<Q", 0x22))
    emul.ecrire_cadre(552, struct.pack("<I", min(384, taille)))

    journal: list = []
    m_tampon = bytearray(disk[:384])
    curseur, vue, rempl = 0x22, 0, min(384, taille)
    m_actif, m_nibble = 0, 0
    divergences = 0
    premieres = []
    rng = random.Random(GRAINE)
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "
    hwnd = 0x770001
    for i in range(10_000):
        tirage = rng.random()
        frappe = VK_SUPPR if tirage < 0.02 else (
            rng.choice(bruit) if tirage < 0.04 else rng.choice(hexa))
        r = frapper(emul, hwnd, frappe)
        if frappe == VK_SUPPR:
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
                        m_tampon[curseur - vue] = octet
                    curseur = min(curseur + 1, taille - 1)
                    nv, relu = m_vue_suit(curseur, vue, taille)
                    if relu:
                        vue = nv
                        rempl = min(384, taille - vue)
                        m_tampon = bytearray(
                            fenetre_editee(disk, journal, vue, rempl))
        probleme = None
        if r["rax"] not in (0, -3):
            probleme = f"le verdict {r['rax']} inattendu"
        attente = struct.unpack("<II", emul.uc.mem_read(L.R_SAISIE + 4, 8))
        if probleme is None and attente != (m_actif, m_nibble if m_actif else 0):
            probleme = "l'attente diverge"
        elif probleme is None and HE.lire_journal(emul) != journal:
            probleme = "le journal diverge"
        elif probleme is None and (emul.u64(544) != curseur
                                   or emul.u64(536) != vue):
            probleme = "le curseur ou la vue divergent"
        elif probleme is None and emul.u32(552) != rempl:
            probleme = "le remplissage diverge"
        elif probleme is None and bytes(
                emul.uc.mem_read(L.R_CADRE + 568, 384)) != bytes(m_tampon):
            probleme = "le tampon diverge"
        elif probleme is None and emul.u32(556) != (1 if journal else 0):
            probleme = "la marque diverge"
        elif probleme is None and emul.u32(560) != 0:
            probleme = "la garde diverge"
        if probleme:
            divergences += 1
            if divergences <= 3:
                consigne = (f"    [{arme}] {probleme} — frappe {i + 1} : "
                            f"la pièce pose vue={emul.u64(536)} "
                            f"curseur={emul.u64(544)}, le modèle tient "
                            f"vue={vue} curseur={curseur}")
                print(consigne)
                premieres.append((i + 1, emul.u64(536), vue, probleme))
    return divergences, premieres


def main() -> int:
    print("=== L'ÉPREUVE DES MÉTRIQUES (L5 — née du ROUGE V1 du terrain v3, "
          "l'Entrée 352) : LE JUGE POSE L'ÉCRAN QU'IL ANNONCE ===")

    # ---- L5-a : LE GESTE STRUCTUREL (le scénario pose-t-il la zone ?) -------
    src = open(SCENARIO_V3, encoding="utf-8").read()
    geste = ("0xFDF0" in src or "0xfdf0" in src
             or "R_METRIQUES" in src or "poser_metriques" in src)
    controle("L5a-le-scenario-pose-l-ecran", geste,
             ("l'écriture à R_METRIQUES [0xFDF0] présente au scénario livré"
              if geste else
              "AUCUNE écriture à R_METRIQUES [0xFDF0] au scénario livré — la "
              "zone vit à son état statique (LES ZÉROS du .data), la pièce "
              "lit lignes=0, la vitrine dégénère à LA VUE MÊME"))

    # ---- la pièce : l'état statique de la zone (constaté octet par octet) ---
    brut = open(os.path.join(UNITE, "kit", "kit-unite-04-d210-20261118-v3",
                             "loupe.exe"), "rb").read()
    e = struct.unpack_from("<I", brut, 0x3C)[0]
    nb = struct.unpack_from("<H", brut, e + 6)[0]
    opt = struct.unpack_from("<H", brut, e + 20)[0]
    rva_stat = None
    for k in range(nb):
        o = e + 24 + opt + k * 40
        va = struct.unpack_from("<I", brut, o + 12)[0]
        vs = struct.unpack_from("<I", brut, o + 8)[0]
        ra = struct.unpack_from("<I", brut, o + 20)[0]
        if va <= 0xFDF0 < va + vs:
            rva_stat = ra + 0xFDF0 - va
    statique = struct.unpack_from("<I", brut, rva_stat + 8)[0]
    print(f"[CONSTAT] le .data livré à R_METRIQUES+8 [0xFDF8] = {statique} "
          f"(l'état statique — personne ne le pose au terrain)")

    # ---- L5-b / L5-c : le différentiel reconstitué contre LA PIÈCE ---------
    temoins = HN.composer_temoins()
    disk = temoins["temoin-3f.bin"]
    os_v = HE.OSEdition()
    for nom, donnees in temoins.items():
        os_v.declarer(nom, HE.FichierEditable(contenu=donnees))
    emul = EmulationCampagne(os_v)

    print("\n-- L5b : LE TERRAIN RECONSTITUÉ (les métriques à leur état "
          "statique — les zéros ; le modèle du juge lignes=27) --")
    div_terrain, prem_terrain = differential(emul, os_v, disk, False, "V1")
    controle("L5b-le-terrain-reconstitue", div_terrain > 0,
             f"{div_terrain} divergences aux 10 000 frappes — le problème « le "
             f"curseur ou la vue divergent » == la console du terrain MOT POUR "
             f"MOT" + (f" ; la PREMIÈRE à la frappe {prem_terrain[0][0]} "
                       f"(la pièce pose vue={prem_terrain[0][1]}, le modèle "
                       f"tient vue={prem_terrain[0][2]})" if prem_terrain else ""))

    print("\n-- L5c : LE LABO RECONSTITUÉ (les métriques POSÉES — 27, le geste "
          "du harnais ; le même modèle) --")
    div_labo, _ = differential(emul, os_v, disk, True, "V1")
    controle("L5c-le-labo-reconstitue", div_labo == 0,
             f"{div_labo} divergence — la pièce N'EST PAS en faute : l'écran "
             f"posé, le différentiel EST VERT (l'état de l'oracle à la "
             f"construction)")

    print(f"\n[BILAN] {VERTS} VERT, {ROUGES} ROUGE — la faute nommée : la "
          f"classe « les-metriques-ecran-jamais-posees-par-le-juge » (le côté "
          f"KIT ; la pièce intacte b382e01b…, per-spec : elle lit l'écran que "
          f"l'hôte doit poser)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
