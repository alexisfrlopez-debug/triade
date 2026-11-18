#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""epreuve_posix_loupe16_d210.py — LE CONTRAT REJOUÉ AU POSIX contre la
pièce C même (l'unité 04 D210, loupe-16 × bras C). Le source PUR ISO C
compile en objet partagé au gcc du labo (gcc -O2 -std=c11 -Wall -Wextra
-shared -fPIC — la commande consignée au LISEZMOI du kit ; la DLL au
terrain se construit par x86_64-w64-mingw32-gcc), l'export
loupe_16_saisie APPELÉ NATURELLEMENT — le juge est le MODÈLE
INDÉPENDANT (le miroir de l'oracle du bras T : les MÊMES vecteurs, la
MÊME graine 20261115).

  V1 le différentiel : 10 000 frappes aux DEUX disques (63 o ET 8 192 o
     — les ré-écritures, la frontière des 256 distincts, la vue qui
     suit, le recouvrement) == le modèle Python à CHAQUE frappe ;
  V2 le scénario « 4d5a » (le journal, le tampon, la marque, la garde,
     la cellule suivante) + LA VUE QUI SUIT (le recadrage, la
     relecture-miroir, le recouvrement) ;
  V3 les rejets : E1 -4 sans session, E2 la fantôme (-3, RIEN au
     journal) ET la fantôme MARCHE SALE (le remplissage u32), le vide,
     E3 le 257e distinct (-3, RIEN perdu) ;
  V4 le repli : le non-hexa ignoré, VK_SUPPR à l'attente ;
  V5 la falsification : la garde non ré-armée (le source muté — la
     ligne refus_quitter = 0 ôtée) — le scénario de loupe-18 (éditer
     puis Alt+F4 UNE SEULE fois doit avertir) ÉCHOUE ; la pièce juste
     re-jouée VERTE.
"""
import ctypes
import pathlib
import random
import struct
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
SOURCE = ICI / "epreuves" / "source-loupe-16-C.c"
GRAINE = 20261115
TAMPON = 384
EDITS = 256

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


# ==================== LE MODÈLE INDÉPENDANT (jamais la pièce) ================


def m_journal_seconde(journal, curseur, octet):
    for i, (dec, _) in enumerate(journal):
        if dec == curseur:
            journal[i] = (curseur, octet)
            return journal, False
    if len(journal) >= EDITS:
        return journal, True
    journal.append((curseur, octet))
    return journal, False


def m_vue_suit(curseur, vue, taille, lignes=27):
    v = min(24, max(0, lignes - 3))
    if vue <= curseur < vue + v * 16:
        return vue, False
    nv = min((max(0, curseur - 176)) & ~15,
             (max(0, taille - TAMPON) + 15) & ~15 if taille > TAMPON else 0)
    return nv, nv != vue


def fenetre_editee(disk, journal, vue, rempl):
    fen = bytearray(disk[vue:vue + rempl])
    for dec, oct_ in journal:
        if vue <= dec < vue + rempl:
            fen[dec - vue] = oct_
    return bytes(fen)


# ==================== LA PIÈCE C NATURELLEMENT ==============================


def compiler(source: pathlib.Path, sortie: pathlib.Path) -> None:
    r = subprocess.run(
        ["gcc", "-O2", "-std=c11", "-Wall", "-Wextra", "-shared", "-fPIC",
         "-o", str(sortie), str(source)],
        capture_output=True, text=True)
    if r.returncode != 0 or r.stderr.strip():
        sys.exit(f"[!] la compilation refuse : {r.stderr[:400]}")


def charger(chemin: pathlib.Path):
    lib = ctypes.CDLL(str(chemin))
    lib.loupe_16_saisie.restype = ctypes.c_longlong
    lib.loupe_16_saisie.argtypes = [
        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
        ctypes.c_uint, ctypes.c_uint]
    return lib.loupe_16_saisie


class Session:
    """Le miroir des zones du plan : le cadre, la saisie, le journal, le disque."""

    def __init__(self, lib, disk: bytes):
        self.lib = lib
        self.disk = bytes(disk)
        self.cadre = bytearray(960)
        struct.pack_into("<Q", self.cadre, 520, len(disk))       # taille
        struct.pack_into("<Q", self.cadre, 528, 0x1000)          # poignée
        struct.pack_into("<Q", self.cadre, 536, 0)                # vue
        struct.pack_into("<Q", self.cadre, 544, 0x22)             # curseur
        struct.pack_into("<I", self.cadre, 552, min(384, len(disk)))
        struct.pack_into("<Q", self.cadre, 568 + 0 if False else 568, 0)
        self.tampon = bytearray(disk[:min(384, len(disk))]) + bytearray(
            max(0, 384 - min(384, len(disk))))
        self.cadre[568:568 + 384] = self.tampon
        self.saisie = bytearray(96)
        self.journal = bytearray(4112)
        struct.pack_into("<I", self.journal, 4096, 0)

    def frappe(self, caractere: int):
        # les zones PASSÉES EN ÉCRITURE (des vues vivantes sur les tampons —
        # la pièce écrit DEDANS, jamais une copie froide)
        cadre = (ctypes.c_char * 960).from_buffer(self.cadre)
        saisie = (ctypes.c_char * 96).from_buffer(self.saisie)
        journal = (ctypes.c_char * 4112).from_buffer(self.journal)
        return self.lib(cadre, saisie, journal, self.disk, 27, caractere)

    def lit(self, off, n=8, zone=None):
        z = self.cadre if zone is None else zone
        return int.from_bytes(bytes(z[off:off + n]), "little")

    def journal_lu(self):
        n = self.lit(4096, 4, self.journal)
        return [(self.lit(16 * i, 8, self.journal),
                 self.journal[16 * i + 8]) for i in range(n)]


def main() -> int:
    print("=== L'ÉPREUVE POSIX — l'unité 04 D210 (loupe-16 × bras C) : le "
          "contrat rejoué contre la pièce C même ===")
    sortie = ICI / "epreuves" / "loupe16c.so"
    sortie.parent.mkdir(exist_ok=True)
    compiler(SOURCE, sortie)
    saisir = charger(sortie)
    print("[gcc] -O2 -std=c11 -Wall -Wextra PROPRE — la pièce C chargée")
    rng = random.Random(GRAINE)
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "

    # ---- V1 : LE DIFFÉRENTIEL — 10 000 frappes aux DEUX disques -------------
    for nom, disk, depart in (("temoin-3f", bytes((i * 7 + 3) & 0xFF
                                                   for i in range(63)), 0x22),
                              ("grand-8k", bytes((i * 31 + 7) & 0xFF
                                                 for i in range(8192)), 0x17E)):
        taille = len(disk)
        s = Session(saisir, disk)
        struct.pack_into("<Q", s.cadre, 544, depart)
        journal, m_tampon = [], bytearray(
            disk[:min(384, taille)].ljust(384, b"\x00"))
        curseur, vue, rempl = depart, 0, min(384, taille)
        m_actif, m_nibble = 0, 0
        divergences = 0
        for _ in range(10_000):
            tirage = rng.random()
            frappe = 0x08 if tirage < 0.02 else (
                rng.choice(bruit) if tirage < 0.04 else rng.choice(hexa))
            r = s.frappe(frappe)
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
                            m_tampon[curseur - vue] = octet
                        curseur = min(curseur + 1, taille - 1) if taille > 1 else 0
                        nv, relu = m_vue_suit(curseur, vue, taille)
                        if relu:
                            vue = nv
                            rempl = min(384, taille - vue)
                            m_tampon = bytearray(
                                fenetre_editee(disk, journal, vue, rempl)
                                .ljust(384, b"\x00"))
            probleme = None
            if r not in (0, -3):
                probleme = f"le verdict {r} inattendu"
            actif, nibble = struct.unpack_from("<II", s.saisie, 4)
            if probleme is None and (actif, nibble) != (
                    m_actif, m_nibble if m_actif else 0):
                probleme = "l'attente diverge"
            elif probleme is None and s.journal_lu() != journal:
                probleme = "le journal diverge"
            elif probleme is None and (s.lit(544) != curseur
                                       or s.lit(536) != vue):
                probleme = "curseur/vue divergent"
            elif probleme is None and s.lit(552, 4) != rempl:
                probleme = "le remplissage diverge"
            elif probleme is None and bytes(
                    s.cadre[568:568 + 384]) != bytes(m_tampon):
                probleme = "le tampon diverge"
            elif probleme is None and s.lit(556, 4) != (1 if journal else 0):
                probleme = "la marque diverge"
            elif probleme is None and s.lit(560, 4) != 0:
                probleme = "la garde diverge"
            if probleme:
                divergences += 1
                if divergences <= 3:
                    print(f"    [{nom}] {probleme}")
        controle(f"V1:le-differentiel-10000-frappes-{nom}", divergences == 0,
                 "le journal PAR DÉCALAGE (la réécriture REMPLACE, la borne "
                 "256 refusée), l'attente CONSOMMÉE, le tampon (le "
                 "recouvrement), la marque, la garde, le pas clampé, LA VUE "
                 "QUI SUIT — tout == le modèle Python")

    # ---- V2 : LE SCÉNARIO « 4d5a » + la vue qui suit ------------------------
    s = Session(saisir, bytes((i * 7 + 3) & 0xFF for i in range(63)))
    for ch in (0x34, 0x64, 0x35, 0x61):
        r = s.frappe(ch)
    controle("V2:le-scenario-4d5a",
              r == 0 and s.lit(544) == 0x24 and s.lit(556, 4) == 1
              and s.lit(560, 4) == 0
              and s.journal_lu() == [(0x22, 0x4D), (0x23, 0x5A)]
              and s.cadre[568 + 0x22] == 0x4D and s.cadre[568 + 0x23] == 0x5A,
              "« 4d5a » : les DEUX octets au journal ET au tampon, la marque, "
              "LA GARDE ré-armée, la cellule suivante active (curseur 0x24)")
    disk = bytes((i * 31 + 7) & 0xFF for i in range(8192))
    s = Session(saisir, disk)
    struct.pack_into("<Q", s.cadre, 544, 0x17E)
    s.frappe(0x34)
    s.frappe(0x41)
    r = s.frappe(0x35)
    r = s.frappe(0x30)
    attendu = fenetre_editee(disk, [(0x17E, 0x4A), (0x17F, 0x50)], 208, 384)
    controle("V2:la-vue-qui-suit-le-recadrage",
             r == 0 and s.lit(544) == 384 and s.lit(536) == 208
             and s.lit(552, 4) == 384
             and bytes(s.cadre[568:568 + 384]) == attendu,
             "le curseur au-delà de la vitrine → la nouvelle vue 208 "
             "(aligne16_inf), LA RELECTURE-MIROIR (le disque + le "
             "recouvrement du journal), remplissage 384 — la cellule suivante "
             "ATTEND à l'écran")

    # ---- V3 : LES REJETS -----------------------------------------------------
    s = Session(saisir, bytes(63))
    struct.pack_into("<Q", s.cadre, 528, (1 << 64) - 1)          # hors session
    r = s.frappe(0x34)
    barre = bytes(s.saisie[12:12 + 80]).split(b"\x00")[0]
    controle("V3:E1-sans-session", r == -4 and barre == b"aucun fichier ouvert",
             "-4, la phrase nommée à la barre (le mode MESSAGE posé)")
    s = Session(saisir, bytes(384))
    struct.pack_into("<Q", s.cadre, 544, 384 + 5)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    actif = struct.unpack_from("<I", s.saisie, 4)[0]
    barre = bytes(s.saisie[12:12 + 80]).split(b"\x00")[0]
    controle("V3:E2-la-cellule-fantome",
             r == -3 and s.lit(4096, 4, s.journal) == 0 and actif == 0
             and barre == b"hors bornes",
             "le curseur forgé au-delà du remplissage → -3, RIEN au journal "
             "(le refus PRÉCÈDE), l'attente CONSOMMÉE")
    struct.pack_into("<I", s.cadre, 556, 1)                     # la marque
    struct.pack_into("<Q", s.cadre, 544, 384 + 5)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:E2-la-fantome-marche-sale",
             r == -3 and s.lit(4096, 4, s.journal) == 0,
             "la marque posée : la fantôme REFUSÉE QUAND MÊME — le "
             "remplissage lu u32 SEUL (jamais le qword)")
    s = Session(saisir, b"")                                    # le vide
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    controle("V3:le-fichier-vide", r == -3 and s.lit(4096, 4, s.journal) == 0,
             "taille zéro : aucune cellule n'existe → -3")
    s = Session(saisir, bytes(384))
    struct.pack_into("<Q", s.cadre, 544, 0x20)
    for i in range(256):                                        # 256 distincts
        struct.pack_into("<Q", s.journal, 16 * i, 0x40 + i)
        s.journal[16 * i + 8] = (i * 7) & 0xFF
    struct.pack_into("<I", s.journal, 4096, 256)
    struct.pack_into("<II", s.saisie, 4, 1, 4)
    r = s.frappe(0x64)
    barre = bytes(s.saisie[12:12 + 80]).split(b"\x00")[0]
    controle("V3:E3-le-257e-distinct",
             r == -3 and s.lit(4096, 4, s.journal) == 256
             and barre == b"journal plein - Ctrl+S",
             "le 257e distinct → -3 nommé, les 256 INTACTS (RIEN perdu)")

    # ---- V4 : LE REPLI ------------------------------------------------------
    for ch in (0x7A, 0x21, 0x20):
        r = s.frappe(ch)
    controle("V4:le-non-hexa-ignore",
             r == 0 and s.lit(4096, 4, s.journal) == 256,
             "« z », « ! », l'espace IGNORÉS proprement (rien bougé)")
    s = Session(saisir, bytes(63))
    s.frappe(0x34)
    s.frappe(0x08)
    actif, nibble = struct.unpack_from("<II", s.saisie, 4)
    r = s.frappe(0x08)
    controle("V4:vk-suppr-a-l-attente",
             actif == 0 and nibble == 0 and r == 0
             and s.lit(4096, 4, s.journal) == 0,
             "« 4 » frappé, VK_SUPPR : le nibble EFFACÉ ; hors attente : "
             "ignoré")

    # ---- V5 : LA FALSIFICATION — la garde non ré-armée -----------------------
    source = SOURCE.read_text(encoding="utf-8")
    cible = "ecrire_u32(cadre, CADRE_REFUS_QUITTER, 0u);"
    if source.count(cible) != 1:
        sys.exit("[!] la ligne de la garde introuvable au source")
    mut = source.replace(cible, "/* le mutant : la garde non ré-armée */")
    chemin_mut = ICI / "epreuves" / "source-loupe-16-C-mut.c"
    chemin_mut.write_text(mut, encoding="utf-8")
    so_mut = ICI / "epreuves" / "loupe16c-mut.so"
    compiler(chemin_mut, so_mut)
    saisir_mut = charger(so_mut)

    def scenario_garde(fonction):
        s2 = Session(fonction, bytes(384))
        struct.pack_into("<I", s2.cadre, 560, 1)     # le premier Alt+F4 refusé
        s2.frappe(0x62)
        r2 = s2.frappe(0x62)                         # « bb » → l'octet 0xBB
        return r2, s2.lit(560, 4)

    r_juste, garde_juste = scenario_garde(saisir)
    r_mut, garde_mut = scenario_garde(saisir_mut)
    controle("V5:la-garde-re-armee-a-l-ecriture",
             r_juste == 0 and garde_juste == 0,
             "la pièce juste : l'écriture RÉ-ARME la garde (refus_quitter = "
             "0) — Alt+F4 une seule fois après l'édition AVERTIRAIT (le "
             "scénario de loupe-18 tient)")
    controle("V5:le-mutant-attrape",
             r_mut == 0 and garde_mut == 1,
             "le mutant (la garde non ré-armée) : la garde DEMEURE 1 — le "
             "scénario Alt+F4 ÉCHOUE (la sortie tranche direct, jamais le "
             "refus -5) — la falsification DEMANDÉE, ATTRAPÉE au bras C")
    r = s.frappe(0x62)
    controle("V5:la-piece-juste-re-jouee",
             r == 0 and s.lit(560, 4) == 0,
             "la pièce juste re-devenue la même — le vert rendu au retrait "
             "de la mutation")

    print(f"\n=== L'ÉPREUVE POSIX {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
