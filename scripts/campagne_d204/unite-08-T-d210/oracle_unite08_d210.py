#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_unite08_d210.py — L'ORACLE DU BLOC AU PÉRIMÈTRE LIVRÉ, l'unité
02 D210 (loupe-08 ligne × bras T — le juge = le modèle indépendant).

LES VECTEURS DEPUIS LE CONTRAT (loupe/I/loupe-08-ligne.md — l'oracle
régénéré depuis I, écrit-avant-code : oracle-depuis-I.txt) : le harnais
du domaine (harnais_noyau.Emulation : le mini-OS, les shims, les
sentinelles) porte la pièce de campagne au slot loupe-08, les
DIX-SEPT autres blocs demeurant les scellés.

  V1 (le doré)       : la première ligne de proxy.exe scellé + la ligne
      finale incomplète du témoin 3 × 64 Kio + 1 (UN octet valide) ;
  V2 (le différentiel) : 10 000 lignes aléatoires (la graine fixe
      20261115, les MÊMES tirages que le juge du terrain D204) == le
      modèle Python OCTET PAR OCTET ; la source LUE SEULE (I3) ;
      EXACTEMENT 77 o écrits, le poison au-delà intact (I2) ; l'état
      propre (rax = 0, les non-volatils, la pile, les canaris) ;
  V3 (les rejets)    : longueur 0, longueur 17, source nulle, sortie
      nulle → les QUATRE verdicts -5, RIEN écrit (la sortie POISON
      INTACTE) ;
  V4 (la falsification) : la colonne décalée d'un espace — le test du
      médian muté (cmp r9d, 8 → 9 : la double espace après le NEUVIÈME
      groupe, la colonne dérive) : les 200 lignes du mutant DIVERGENT ;
      la notation juste rejouée VERTE au retrait de la mutation.

LA TABLE R_HEX (0x2050) : relue AU FICHIER DE LA PIÈCE LIVRÉE (le
recoup — la pièce la porte à SON .rdata) puis posée au harnais (le
désert du noyau nommé à la D204, le miroir de harnais_rendu).

Usage : python3 scripts/campagne_d204/unite-08-T-d210/oracle_unite08_d210.py
Sortie : 0 = oracle VERT (falsification comprise) ; 2 = refus nommé.
"""
from __future__ import annotations

import hashlib
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-08-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN          # noqa: E402  (le harnais du domaine)
import build_loupe as BL            # noqa: E402  (B4 : le lecteur canonique)

L = HN.L
B4 = HN.B4

NOTATION = os.path.join(UNITE, "notation", "loupe-08-ligne.asm")
GRAINE = 20261115                    # la graine fixe des lignes aléatoires
ADRESSE_SOURCE = 0x700600           # 16 o : la source du geste
ADRESSE_SORTIE = 0x700700           # 96 o : la ligne empoisonnée
POISON = b"\xCC"

VERTS, ROUGES = 0, 0


def controle(nom: str, ok: bool, detail: str = "") -> None:
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def refus(nom: str, detail: str) -> None:
    print(f"[oracle-unite08-d210] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


def modele_ligne(decalage: int, octets: bytes) -> bytes:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat (oracle-depuis-I),
    jamais les octets du bloc : la ligne de 77 o exacts."""
    s = f"{decalage:08X}  "
    g = [f"{b:02X}" if i < len(octets) else "  "
         for i, b in enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(g[:8]) + "  " + " ".join(g[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"          # 77 o exacts


class EmulationCampagne(HN.Emulation):
    """Le harnais du domaine au slot loupe-08 PORTANT LA PIÈCE DE
    CAMPAGNE : les dix-sept autres blocs demeurent les notations
    scellées (la feuille pure n'est appelée par aucun d'eux au périmètre
    livré)."""

    def __init__(self, os_virtuel, notation=NOTATION):
        super().__init__(os_virtuel)
        rva, slot = L.SLOTS_LOUPE["i110008"]
        if not os.path.exists(notation):
            refus("NOTATION-ABSENTE", f"{notation} — construire d'abord")
        octets, metas = B4.assembler_bloc(self.ks, notation, rva, slot)
        self.uc.mem_write(rva, octets)
        self.blobs["i110008"] = (octets, metas)
        # LA TABLE HEXA DU PLAN posée au harnais (I4 — le noyau ne porte
        # que les tables MD5 : le désert nommé à la D204, le miroir de
        # harnais_rendu) ; la PIÈCE, elle, la porte à SON .rdata 0x2050 —
        # recoupée au FICHIER LIVRÉ même avant la pose
        piece = os.path.join(UNITE, "piece", "loupe.exe")
        if not os.path.exists(piece):
            refus("PIÈCE-ABSENTE", f"{piece} — construire d'abord")
        brut = open(piece, "rb").read()
        import struct as _s
        e = _s.unpack_from("<I", brut, 0x3C)[0]
        nb = _s.unpack_from("<H", brut, e + 6)[0]
        opt = _s.unpack_from("<H", brut, e + 20)[0]
        posee = None
        for k in range(nb):
            o = e + 24 + opt + k * 40
            va = _s.unpack_from("<I", brut, o + 12)[0]
            vs = _s.unpack_from("<I", brut, o + 8)[0]
            ra = _s.unpack_from("<I", brut, o + 20)[0]
            if va <= L.R_HEX < va + vs:
                posee = brut[ra + L.R_HEX - va:ra + L.R_HEX - va + 17]
        if posee != b"0123456789ABCDEF\x00":
            refus("TABLE-HORS-PIÈCE",
                  "le .rdata de la pièce ne porte pas la table du plan à "
                  "0x2050 — la pièce est fausse, jamais le harnais")
        self.uc.mem_write(L.R_HEX, b"0123456789ABCDEF\x00")


def composer(emul: HN.Emulation, source: bytes, longueur: int,
             decalage: int, sortie=ADRESSE_SORTIE):
    """Le geste de la campagne : la sortie POISONNÉE à 96 o avant l'appel
    (les refus ne publient RIEN, jamais un de plus), la ligne lue après."""
    emul.uc.mem_write(ADRESSE_SOURCE, source)
    emul.uc.mem_write(sortie, POISON * 96)
    r = emul.appeler(L.LOUPE08_VA, {"rcx": ADRESSE_SOURCE,
                                    "rdx": longueur,
                                    "r8": sortie,
                                    "r9": decalage})
    return r, bytes(emul.uc.mem_read(sortie, 96))


def main() -> int:
    print("=== L'ORACLE DU BLOC — l'unité 02 D210 (loupe-08 × bras T) : "
          "les vecteurs du contrat, le juge = le modèle indépendant ===")
    os_v = HN.OSVirtuel()
    emul = EmulationCampagne(os_v)

    # LES ANCRES R7 RELUES (le harnais du domaine les exige — la feuille
    # pure ne les appelle pas, l'image les porte)
    m9 = open(os.path.join(HN.TRIADE, HN.SCELLE_M9), "rb").read()
    m1 = open(os.path.join(HN.TRIADE, HN.SCELLE_M1), "rb").read()
    if hashlib.sha256(m9).hexdigest() != HN.SCELLE_M9_SHA256 \
            or hashlib.sha256(m1).hexdigest() != HN.SCELLE_M1_SHA256:
        refus("SCELLÉS-DIVERGENTS", "M1/M9 != les ancres du harnais")
    emul.poser_heritages(m9, m1)

    # ---- V1 : LE DORÉ — la première ligne du scellé + la ligne finale ------
    print("\n-- V1 : le doré (la pièce de l'ère à l'œil, la ligne finale) --")
    premiere = m9[:16]                       # « MZ\x90\x00\x03\x00… »
    r, ligne = composer(emul, premiere, 16, 0)
    attendu = modele_ligne(0, premiere)
    ok = (r["rax"] == 0 and emul.etat_propre(r)
          and ligne[:77] == attendu and ligne[77:] == POISON * 19)
    controle("V1:le-dore-proxy-premiere-ligne", ok,
             f"les 77 o == le modèle ({premiere[:6].hex()}…, "
             f"« {attendu[:34].decode('latin-1')}… »)")

    temoins = HN.composer_temoins()
    finale = temoins["temoin-3f.bin"][-1:]   # 3 × 64 Kio + 1 : le dernier octet
    r, ligne = composer(emul, finale, 1, 3 * 65536)
    attendu = modele_ligne(3 * 65536, finale)
    ok = (r["rax"] == 0 and emul.etat_propre(r)
          and ligne[:77] == attendu and ligne[77:] == POISON * 19)
    controle("V1:le-témoin-3f-ligne-finale-incomplète", ok,
             "UN octet valide : quinze groupes d'espaces, la colonne "
             "ASCII droite — Q3")

    # ---- V2 : LE DIFFÉRENTIEL — 10 000 lignes aléatoires -------------------
    print("\n-- V2 : le différentiel (10 000 lignes, la graine fixe) --")
    rng = random.Random(GRAINE)
    ecarts, ecarts_source, ecarts_poison, ecarts_etat = 0, 0, 0, 0
    for _ in range(10_000):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = bytes(rng.randrange(0, 100) % 256 for _ in range(16))
        r, ligne = composer(emul, source, longueur, decalage)
        attendu = modele_ligne(decalage, source[:longueur])
        if ligne[:77] != attendu:
            ecarts += 1
        if bytes(emul.uc.mem_read(ADRESSE_SOURCE, 16)) != source:
            ecarts_source += 1                       # I3 : la source lue seule
        if ligne[77:] != POISON * 19:
            ecarts_poison += 1                       # I2 : jamais un de plus
        if not emul.etat_propre(r) or r["rax"] != 0:
            ecarts_etat += 1
    controle("V2:le-différentiel-10-000-lignes", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle, "
             f"{ecarts} écart(s)")
    controle("V2:la-source-lue-seule", ecarts_source == 0,
             "les octets de la source INTACTS aux 10 000 gestes (I3)")
    controle("V2:exactement-77-o", ecarts_poison == 0,
             "le poison au-delà de 77 demeure (I2 : jamais un de plus)")
    controle("V2:l'état-propre", ecarts_etat == 0,
             "rax = 0, les non-volatils rendus, la pile équilibrée, les "
             "canaris intacts")

    # ---- V3 : LES REJETS — les quatre -5, RIEN écrit ------------------------
    print("\n-- V3 : les rejets (E1/E2/E3 — rien écrit) --")
    source16 = bytes(range(0x10, 0x20))
    emul.uc.mem_write(ADRESSE_SOURCE, source16)
    for nom, args in (
            ("E1:la-longueur-nulle", {"rcx": ADRESSE_SOURCE, "rdx": 0,
                                      "r8": ADRESSE_SORTIE, "r9": 0}),
            ("E2:la-longueur-dix-sept", {"rcx": ADRESSE_SOURCE, "rdx": 17,
                                         "r8": ADRESSE_SORTIE, "r9": 0}),
            ("E3:la-source-nulle", {"rcx": 0, "rdx": 5,
                                    "r8": ADRESSE_SORTIE, "r9": 0}),
            ("E3:la-sortie-nulle", {"rcx": ADRESSE_SOURCE, "rdx": 5,
                                    "r8": 0, "r9": 0})):
        emul.uc.mem_write(ADRESSE_SORTIE, POISON * 96)
        r = emul.appeler(L.LOUPE08_VA, args)
        intact = bytes(emul.uc.mem_read(ADRESSE_SORTIE, 96)) == POISON * 96
        controle(f"V3:{nom}", r["rax"] == -5 and intact
                 and emul.etat_propre(r),
                 f"verdict {r['rax']}, la sortie POISON INTACTE")

    # ---- V4 : LA FALSIFICATION DEMANDÉE — la table décalée d'un octet -------
    print("\n-- V4 : la falsification (la table hexa décalée d'un octet) --")
    texte = open(NOTATION, encoding="utf-8").read()
    cible = "lea r11, [rip - 0x29a0]"
    if texte.count(cible) != 1:
        refus("MUTATION-INTROUVABLE",
              f"« {cible} » attendu UNE fois dans la notation")
    mution = texte.replace(cible, "lea r11, [rip - 0x29a1]")
    # LA TABLE DÉCALÉE D'UN OCTET : le pointeur du plan vise 0x204F au lieu
    # de R_HEX 0x2050 — chaque chiffre hexa lit la MAUVAISE entrée : TOUTE
    # ligne à contenu diverge du modèle (le médian décalé — la première
    # mutation tentée — ne déplaçait PAS les colonnes : la redistribution
    # des séparateurs totalise le même compte d'espaces, la falsification
    # invisible aux longueurs courtes, NOMMÉE puis remplacée)
    chemin_mut = os.path.join(UNITE, "epreuves", "falsifiee-table.asm")
    os.makedirs(os.path.dirname(chemin_mut), exist_ok=True)
    with open(chemin_mut, "w", encoding="utf-8") as f:
        f.write(mution)
    emul_mut = EmulationCampagne(HN.OSVirtuel(), notation=chemin_mut)
    emul_mut.poser_heritages(m9, m1)
    rng = random.Random(GRAINE)
    pris = 0
    for _ in range(200):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = bytes(rng.randrange(0, 256) for _ in range(16))
        r, ligne = composer(emul_mut, source, longueur, decalage)
        if ligne[:77] != modele_ligne(decalage, source[:longueur]):
            pris += 1
    controle("V4:la-table-décalée-attrapée", pris == 200,
             "les 200 lignes du mutant DIVERGENT du modèle — la "
             "falsification est DÉTECTABLE (la table ne bouge jamais, "
             "la faute si)")
    r, ligne = composer(emul, m9[:16], 16, 0)
    controle("V4:la-notation-juste-rejouée", r["rax"] == 0
             and ligne[:77] == modele_ligne(0, m9[:16]),
             "la pièce de campagne redevenue la même — le vert rendu au "
             "retrait de la mutation")

    print(f"\n=== L'ORACLE {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
