#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite13.py — L'ORACLE DU BLOC AU PÉRIMÈTRE LIVRÉ, l'unité 5
(loupe-13 recherche × bras T, la campagne D204 — le juge = le modèle
indépendant).

LES VECTEURS DEPUIS LE CONTRAT (loupe/I/loupe-13-recherche.md — l'oracle
écrit-avant-code) : le harnais du domaine (harnais_noyau.Emulation : le
mini-OS, les shims, les sentinelles) porte la pièce de campagne au slot
loupe-13, les dix-sept autres blocs demeurant les scellés — la feuille pure
n'appelle que LIBC-02, AUCUNE feuille IAT ne vit au bloc.

  V1 (le doré)        : LE CORPUS DE L'ÉCOLE (le motif au premier octet, au
      dernier, à cheval sur le départ, l'occurrence DOUBLE — LA PREMIÈRE
      exigée, le motif répétitif « AAAA » dans « AAAAB », le presque-frère,
      le départ au milieu, la fenêtre vide, la plage vide, le motif plus
      long que la plage restante) + LES MARQUES DE PROXY.EXE SCELLÉ sur sa
      première fenêtre de 8 192 o (MZ, PE, « This program » — chaque
      position == bytes.find ; « PEMax » la marque inventée → LA FIN NOMMÉE
      -1, l'absence constatée) ;
  V2 (le différentiel): 10 000 cas aléatoires (fenêtres 0..4 096 o, motifs
      1..32, départs aléatoires, alphabet plein 0x00-0xFF ET alphabet
      pauvre pour forcer les occurrences multiples — la graine fixe
      20261115, les MÊMES tirages au terrain) : rax == bytes.find À
      L'IDENTIQUE, y compris les -1 (Q1-Q4) ; la fenêtre et le motif LUS
      SEULS (I3), l'état propre aux 10 000 gestes (I4 : les non-volatils
      rendus, la pile équilibrée, les canaris intacts) ;
  V3 (les rejets)     : le motif vide, le motif de 33 o, le départ au-delà
      → les TROIS verdicts -5, l'état propre ;
  V4 (la falsification): LA POSITION AVANCÉE D'UN (mov rax, rbx → lea rax,
      [rbx + 1] dans la notation — le second match au lieu du premier) :
      chaque cas à occurrence DIVERGE du modèle — la falsification DEMANDÉE
      par le contrat ; la notation juste REJOUÉE VERTE au retrait de la
      mutation.

Usage : python3 scripts/campagne_d204/unite-13-T/oracle_unite13.py
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
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-13-T")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

import importlib.util as _ilu       # noqa: E402  (l'auteur, pour le mutant)
# le plan loupe chargé sous LE NOM « layout » (la leçon D158 : le nom est
# disputé par la chaîne m4 — l'auteur fait « import layout », jamais
# d'anonyme), puis l'auteur, puis le monde tel qu'il était
_sys_layout = sys.modules.get("layout")
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L_layout = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L_layout
_spec_l.loader.exec_module(L_layout)
_spec_a = _ilu.spec_from_file_location(
    "auteur_oracle13", os.path.join(REPO, "loupe", "outils", "auteur.py"))
AUTEUR = _ilu.module_from_spec(_spec_a)
sys.modules["auteur_oracle13"] = AUTEUR
_spec_a.loader.exec_module(AUTEUR)
if _sys_layout is not None:
    sys.modules["layout"] = _sys_layout   # le monde tel qu'il était
else:
    del sys.modules["layout"]

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(UNITE, "notation", "loupe-13-recherche.asm")
GRAINE = 20261115                    # la graine fixe des tirages (T == terrain)
ADRESSE_FENETRE = 0x710000           # la fenêtre de test (4 096 o + la marge)
ADRESSE_MOTIF = 0x730000             # le motif de test (32 o + la garde)
FENETRE_PROXY = 8192                 # la première fenêtre du scellé

VERTS, ROUGES = 0, 0


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def refus(nom: str, detail: str) -> None:
    print(f"[oracle-unite13] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


def modele_recherche(fenetre: bytes, motif: bytes, depart: int) -> int:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat (l'écrit-avant-code),
    jamais les octets du bloc : la position ABSOLUE de la première
    occurrence, ou les verdicts nommés."""
    if len(motif) < 1 or len(motif) > 32:
        return -5                                  # E1/E2 : la borne P4
    if depart > len(fenetre):
        return -5                                  # E3 : le départ est une position
    if len(motif) > len(fenetre) - depart:
        return -1                                  # Q2 : le constat trivial
    return fenetre.find(motif, depart)             # Q1/Q3/Q4 : la première


def extraire_m1(donnees: bytes, rva: int, taille: int) -> bytes:
    """L'extrait du scellé M1 à sa RVA d'origine (le parse minimal des
    sections PE — le geste du chantier (c) rejoué : libc-02 vit à SON
    adresse scellée dans l'image loupe comme dans selftest.exe)."""
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    nb = struct.unpack_from("<H", donnees, e + 6)[0]
    opt = struct.unpack_from("<H", donnees, e + 20)[0]
    for i in range(nb):
        o = e + 24 + opt + i * 40
        va, = struct.unpack_from("<I", donnees, o + 12)
        ra, = struct.unpack_from("<I", donnees, o + 20)
        vs, = struct.unpack_from("<I", donnees, o + 8)
        if va <= rva < va + vs:
            raw = ra + (rva - va)
            return donnees[raw:raw + taille]
    refus("RVA-M1-INTROUVABLE", f"la RVA {rva:#x} hors du scellé M1")


class EmulationCampagne(HN.Emulation):
    """Le harnais du domaine au slot loupe-13 PORTANT LA PIÈCE DE CAMPAGNE :
    les dix-sept autres blocs demeurent les notations scellées (la feuille
    pure n'est appelée par aucun d'eux au périmètre livré) ; l'appelant
    factice étendu pose le 5e argument À LA PILE ([rsp+0x28] — P5)."""

    def __init__(self, os_virtuel, notation=NOTATION, verifier_piece=True):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110013"]
        if not os.path.exists(notation):
            refus("NOTATION-ABSENTE", f"{notation} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, notation, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110013"] = (octets, metas)
        if not verifier_piece:
            # le mutant de la falsification : posé sans la pièce (le juge
            # éprouve SES octets à lui — la pièce juste demeure la référence)
            self.uc.mem_map(ADRESSE_FENETRE, 0x21000)
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
                  "le slot loupe-13 de la pièce ne porte pas la notation "
                  "de campagne + le padding NOP — la pièce est fausse")
        # la zone des grands témoins (fenêtre + motif), la marge du noyau
        self.uc.mem_map(ADRESSE_FENETRE, 0x21000)

    def appeler(self, va: int, args: dict | None = None,
                pile_args: list | None = None):
        """L'appelant factice étendu : pile_args pose les arguments AU-DELÀ
        du quatrième à [rsp+0x28+8k] (le 5e de loupe-13 — P5) ; le canari
        couvre la zone AU-DESSUS des arguments (jamais un faux échec par la
        place de l'argument)."""
        if not pile_args:
            return super().appeler(va, args)
        uc = self.uc
        for nom, val in HN.SENTINELLES_NV.items():
            uc.reg_write(HN.REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(HN.REGS[nom], val)
        uc.reg_write(HN.UC_X86_REG_RAX, 0)
        rsp = HN.ENTREE_RSP
        uc.reg_write(HN.UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp, struct.pack("<Q", HN.RET_MAGIQUE))
        uc.mem_write(rsp + 8, HN.CANARI * 0x170)
        for k, val in enumerate(pile_args):
            uc.mem_write(rsp + 0x28 + 8 * k, struct.pack("<Q", val))
        entree_rsp = rsp
        try:
            uc.emu_start(va, HN.RET_MAGIQUE, count=200_000_000)
        except HN.UcError as err:
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


def chercher(emul: EmulationCampagne, fenetre: bytes, motif: bytes,
             depart: int):
    """Le geste de la campagne : la fenêtre et le motif posés, le bloc
    appelé à son adresse au plan, le 5e argument À LA PILE."""
    emul.uc.mem_write(ADRESSE_FENETRE, fenetre)
    emul.uc.mem_write(ADRESSE_MOTIF, motif)
    return emul.appeler(L.LOUPE13_VA, {
        "rcx": ADRESSE_FENETRE, "rdx": len(fenetre),
        "r8": ADRESSE_MOTIF, "r9": len(motif)}, pile_args=[depart])


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 5 (loupe-13 × bras T) : les "
          "vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v = HN.OSVirtuel()
    emul = EmulationCampagne(os_v)

    # LES ANCRES R7 RELUES (le harnais du domaine les exige — la feuille
    # pure ne les appelle pas, l'image les porte) ; LIBC-02 POSE @0x1180
    # (le geste du chantier (c) rejoué : le harnais noyau ne porte que
    # libc-01/07, la feuille de recherche L'EXIGE — l'extrait du scellé M1
    # à son adresse, la pièce l'appelle, le scellé répond)
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
    if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
            or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
        refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
    emul.poser_heritages(m9, m1)
    libc02 = extraire_m1(m1, L.R_LIBC02, 0x80)
    emul.uc.mem_write(L.R_LIBC02, libc02)
    # la double preuve étendue : le LIBC-02 posé == celui de LA PIÈCE
    brut_piece = open(os.path.join(UNITE, "piece", "loupe.exe"), "rb").read()
    e = struct.unpack_from("<I", brut_piece, 0x3C)[0]
    nb = struct.unpack_from("<H", brut_piece, e + 6)[0]
    opt = struct.unpack_from("<H", brut_piece, e + 20)[0]
    piece_libc02 = None
    for k in range(nb):
        o = e + 24 + opt + k * 40
        va = struct.unpack_from("<I", brut_piece, o + 12)[0]
        vs = struct.unpack_from("<I", brut_piece, o + 8)[0]
        ra = struct.unpack_from("<I", brut_piece, o + 20)[0]
        if va <= L.R_LIBC02 < va + vs:
            piece_libc02 = brut_piece[ra + L.R_LIBC02 - va:
                                      ra + L.R_LIBC02 - va + 0x80]
    assert piece_libc02 == libc02, \
        "le libc-02 de la pièce != l'extrait du scellé M1 (R7 rompu)"
    print(f"[R7] libc-02 posé @0x1180 : {len(libc02)} o du scellé M1, "
          "== la pièce — la double preuve")

    # ---- V1 : LE DORÉ — le corpus de l'école + les marques du scellé ------
    print("\n-- V1 : le doré (l'école, les marques de la pièce de l'ère) --")
    ecole = [
        (b"premiere-occurrence", b"premiere", 0, 0),    # le motif au premier octet
        (b"premiere-occurrence", b"occurrence", 0, 9),  # au dernier
        (b"XXabcYY", b"abc", 2, 2),                     # à cheval sur le départ
        (b"abcXabc", b"abc", 0, 0),                     # l'occurrence DOUBLE : LA PREMIÈRE
        (b"AAAAB", b"AAAA", 0, 0),                      # le motif répétitif
        (b"AAAAB", b"AAAB", 0, 1),                      # le presque-frère
        (b"abcabcabc", b"abc", 4, 6),                   # le départ au milieu (la PREMIÈRE depuis lui : @6, jamais @3)
        (b"", b"A", 0, -1),                             # la fenêtre vide
        (b"abc", b"abc", 3, -1),                        # la plage vide (Q3)
        (b"abcd", b"cdef", 2, -1),                      # le motif > la plage restante
    ]
    ecarts_ecole = []
    for fenetre, motif, depart, attendu in ecole:
        r = chercher(emul, fenetre, motif, depart)
        if r["rax"] != attendu or not emul.etat_propre(r):
            ecarts_ecole.append((fenetre, motif, depart, r["rax"]))
    controle("V1:le-corpus-de-l-ecole", not ecarts_ecole,
             f"{len(ecole) - len(ecarts_ecole)}/{len(ecole)} == le modèle "
             "(le premier octet, le dernier, à cheval sur le départ, "
             "l'occurrence DOUBLE — la PREMIÈRE exigée, AAAA dans AAAAB, le "
             "presque-frère, le départ au milieu, la fenêtre vide → -1, la "
             "plage vide → -1, le motif trop long → -1 IMMÉDIAT)"
             + (f" — ÉCARTS : {ecarts_ecole}" if ecarts_ecole else ""))

    proxy8k = m9[:FENETRE_PROXY]
    marques = [(b"MZ", proxy8k.find(b"MZ")),
               (b"PE\x00\x00", proxy8k.find(b"PE\x00\x00")),
               (b"This program", proxy8k.find(b"This program")),
               (b"PEMax", proxy8k.find(b"PEMax"))]     # la marque inventée : -1
    ecarts_marques = []
    for motif, attendu in marques:
        r = chercher(emul, proxy8k, motif, 0)
        if r["rax"] != attendu or not emul.etat_propre(r):
            ecarts_marques.append((motif, attendu, r["rax"]))
    controle("V1:les-marques-de-proxy", not ecarts_marques,
             f"MZ @0, PE @+{marques[1][1]}, « This program » @+{marques[2][1]} "
             "— chaque position == bytes.find sur la première fenêtre du "
             "scellé ; « This program » et « PEMax » les marques ABSENTES "
             "du scellé (les en-têtes écrits à la main) → -1 LA FIN NOMMÉE, "
             "l'absence constatée"
             + (f" — ÉCARTS : {ecarts_marques}" if ecarts_marques else ""))

    # ---- V2 : LE DIFFÉRENTIEL — 10 000 cas aléatoires ----------------------
    print("\n-- V2 : le différentiel (10 000 cas, la graine fixe) --")
    rng = random.Random(GRAINE)
    ecarts, ecarts_lecture, ecarts_etat, cas_nommes = 0, 0, 0, 0
    for _ in range(10_000):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        r = chercher(emul, fenetre, motif, depart)
        attendu = modele_recherche(fenetre, motif, depart)
        if r["rax"] != attendu:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart : n={n} m={m} départ={depart} → "
                      f"{r['rax']} != {attendu}")
        if r["rax"] >= 0:
            cas_nommes += 1            # l'occurrence VRAIE (Q4)
        if bytes(emul.uc.mem_read(ADRESSE_FENETRE, n)) != fenetre \
                or bytes(emul.uc.mem_read(ADRESSE_MOTIF, m)) != motif:
            ecarts_lecture += 1        # I3 : la fenêtre et le motif lus seuls
        if not emul.etat_propre(r):
            ecarts_etat += 1           # I4 : les non-volatils rendus
    controle("V2:le-differentiel-10-000-cas", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (y compris les -1 — "
             f"Q1-Q4 ; {cas_nommes} occurrences VRAIES), "
             f"alphabets plein ET pauvre, la graine {GRAINE}")
    controle("V2:la-fenetre-et-le-motif-lus-seuls", ecarts_lecture == 0,
             "les octets de la fenêtre et du motif INTACTS aux 10 000 "
             "gestes (I3 — la pureté)")
    controle("V2:l-etat-propre", ecarts_etat == 0,
             "les non-volatils rendus, la pile équilibrée, les canaris "
             "intacts aux 10 000 gestes (I4)")

    # ---- V3 : LES REJETS — les trois -5 ------------------------------------
    print("\n-- V3 : les rejets (E1/E2/E3) --")
    fenetre4 = b"ABCD"
    for nom, motif, depart in (
            ("E1:le-motif-vide", b"", 0),
            ("E2:le-motif-de-trente-trois", b"X" * 33, 0),
            ("E3:le-depart-au-dela", b"A", 5)):
        r = chercher(emul, fenetre4, motif, depart)
        controle(f"V3:{nom}", r["rax"] == -5 and emul.etat_propre(r),
                 f"verdict {r['rax']} — chercher rien n'est pas chercher ; "
                 "la borne du quotidien MOTIF_MAX ; le départ est une "
                 "position, pas un vœu")

    # ---- V4 : LA FALSIFICATION DEMANDÉE — la position avancée d'un ---------
    print("\n-- V4 : la falsification (la position avancée d'un) --")
    # LA MUTATION AU BROUILLON, PUIS LA RÉSOLUTION ENTIÈRE REJOUÉE : le
    # mutant est UNE VRAIE NOTATION (les étiquettes re-résolues à la
    # mesure du lea 4 o contre le mov 3 o), jamais un texte balafré aux
    # sauts périmés
    brouillon = open(os.path.join(UNITE, "brouillons",
                                  "loupe-13-recherche.asm"),
                     encoding="utf-8").read()
    cible = "mov rax, rbx"
    if brouillon.count(cible) != 1:
        refus("MUTATION-INTROUVABLE",
              f"« {cible} » attendu UNE fois dans le brouillon")
    mutation = brouillon.replace(cible,
                                 "lea rax, [rbx + 1]")   # la position + 1
    dossier_brouillons_mut = os.path.join(UNITE, "epreuves", "brouillons-mut")
    dossier_notation_mut = os.path.join(UNITE, "epreuves")
    os.makedirs(dossier_brouillons_mut, exist_ok=True)
    with open(os.path.join(dossier_brouillons_mut, "falsifiee-position.asm"),
              "w", encoding="utf-8") as f:
        f.write(mutation)
    AUTEUR.BROUILLONS = dossier_brouillons_mut
    AUTEUR.SORTIE = dossier_notation_mut
    AUTEUR.NOMS_COURTS["falsifiee-position"] = (
        "la recherche : la position avancée d'un (LE MUTANT de la "
        "falsification)")
    rva13, slot13 = L.SLOTS_LOUPE["i110013"]
    deps13 = ("AUCUNE entrée IAT (la feuille pure) ; libc-02 memcmp (LE "
              "BLOC SCELLÉ M1 PAR LA CARTE) ; la falsification : la "
              "position avancée d'un")
    try:
        AUTEUR.resoudre_bloc(
            BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64), "falsifiee-position",
            "i110013", "loupe-13:R1", rva13, slot13, deps13)
    except AUTEUR.ErreurAuteur as exc:
        refus("RÉSOLUTION-AUTEUR-MUTANT", str(exc))
    chemin_mut = os.path.join(dossier_notation_mut, "falsifiee-position.asm")
    emul_mut = EmulationCampagne(HN.OSVirtuel(), notation=chemin_mut,
                                 verifier_piece=False)
    emul_mut.poser_heritages(m9, m1)
    emul_mut.uc.mem_write(L.R_LIBC02, libc02)   # l'ancre du scellé, comme au juge
    rng = random.Random(GRAINE)
    pris, avec_occurrence = 0, 0
    for _ in range(300):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        r = chercher(emul_mut, fenetre, motif, depart)
        attendu = modele_recherche(fenetre, motif, depart)
        if attendu >= 0:
            avec_occurrence += 1
            if r["rax"] != attendu:
                pris += 1              # le mutant rend la position + 1
    controle("V4:la-position-avancee-d-un-attrapee", pris == avec_occurrence,
             f"les {pris}/{avec_occurrence} cas à occurrence DIVERGENT du "
             "modèle — le mutant rend le second match au lieu du premier, "
             "la différentielle ATTRAPE LE FAUX (la falsification "
             "DEMANDÉE par le contrat)")
    r = chercher(emul, proxy8k, b"MZ", 0)
    controle("V4:la-notation-juste-rejouee", r["rax"] == 0
             and emul.etat_propre(r),
             "la pièce de campagne redevenue la même — le vert rendu au "
             "retrait de la mutation (MZ @0, la première occurrence)")

    print(f"\n=== L'ORACLE {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
