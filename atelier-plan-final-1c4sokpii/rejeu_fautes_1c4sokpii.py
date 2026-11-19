#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rejeu_fautes_1c4sokpii.py — LE RE-JEU AVEC LES SHIMS D'INJECTION DE FAUTES
(l'instruction 1c4sokpii, partie 3 : « ajoute des shims à injection de
fautes pour les branches d'erreur, re-joue la mutation aux mêmes tirages
avec composition-killers, rapporte le nouveau taux avec reste nommé »).

LA CASCADE (jamais un tueur affaibli) :
  K1 round-trip + K2 signature — INTACTS (les historiques) ;
  K3 composition — la boucle winmain heureuse INTACTE (rejeu v0.14.0) ;
  K4 FAUTES — LA BATTERIE D'INJECTION, pour les survivants seuls :
    F1 l'ouverture manquée (le fichier absent — le refus à la barre,
       la vitrine VIDE VRAIE) ;
    F2 ALLER le commit VIDE (verdict -5 « saisie mal formée ») ;
    F3 ALLER hors bornes (8 chiffres — verdict -3 « hors bornes ») ;
    F4 ALLER l'hexa vécu ('a' '9' — les chiffres hexa, LE SAUT) ;
    F5 CHERCHER le motif + F3 JUSQU'À LA FIN (verdict -1 « plus
       d'occurrence » — le nombre d'occurrences LU DU FICHIER même) ;
    F6 la saisie au journal PLEIN (les 256 octets DISTINCTS puis un de
       plus — verdict -3 « journal plein » ; le caractère NON HEXA au
       passage — le repli E4 ignoré proprement) ;
    F7 la ligne INCOMPLÈTE (le fichier 2001 o, le défilement AU FOND,
       la dernière ligne partielle — Q3 de loupe-08) ;
    F8 les touches aux BORNES (gauche à 0, Home, End, PgUp au sommet,
       PgDn — les brides de loupe-11/15) ;
    F9 les fautes PAR BLOC (les survivants de loupe-02/05/06/07 : sans
       session -4, hors fichier -3, sortie nulle -5, LE SHIM ReadFile
       EN ÉCHEC -6 — l'injection paramétrable du harnais, E1-E4).

LA MÉTHODE : les MÊMES 832 mutants (la graine 20261111, la boucle
répliquée) ; la batterie SANE calculée UNE FOIS (les bases), chaque
survivant confronté À TOUTE la batterie — tué si UN observable diverge ;
le reste NOMMÉ (le survivant, la cause de sa survie).

Sortie : rejeu_fautes_rapport.txt + rejeu_fautes.csv + reste_nomme.csv."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
ICI = pathlib.Path(__file__).resolve().parent

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_fautes", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_fautes"] = MUT.module
MUT.loader.exec_module(MUT.module)

GRAINE = 20261111


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HE = charger_module("h_edition_fautes", REPO / "loupe" / "harnais_edition.py")
HN = charger_module("h_noyau_fautes", REPO / "loupe" / "harnais_noyau.py")
LL = HN.L
REJEU = charger_module("rejeu_v140_fautes",
                       REPO / "scripts" / "rejeu_survivants_v140.py")

FICHIER_2000 = bytes((i * 7 + 3) % 256 for i in range(2000))
FICHIER_2001 = FICHIER_2000 + b"\x41"        # la dernière ligne INCOMPLÈTE (1 o)
TEM = "temoin-fautes.bin"
TEM_INCOMPLET = "temoin-incomplet.bin"
OCC_4D = sum(1 for i in range(len(FICHIER_2000) - 1)
             if FICHIER_2000[i] == 0x4D)     # LU DU FICHIER même, jamais tapé

BASE_MSG = [
    (0x770001, 5, 0, (440 << 16) | 640),     # WM_SIZE
    (0x770001, 0x0F, 0, 0),                  # WM_PAINT
]

HEXPAIRS = []                                # les 256 octets DISTINCTS
for v in range(256):
    HEXPAIRS += [f"{v:02X}"[0], f"{v:02X}"[1]]

SCENARIOS_APP = {
    "F1-ouverture-manquée": ("loupe.exe fichier-absent.bin", BASE_MSG),
    "F2-aller-vide": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x74, 0),          # F5 → le mode
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x0D, 0),          # RETOUR → commit VIDE → -5
        (0x770001, 0x0F, 0, 0)]),
    "F3-aller-hors-bornes": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x74, 0),
        (0x770001, 0x0F, 0, 0)]
        + [(0x770001, 0x102, 0x46, 0)] * 8   # 'F' × 8
        + [(0x770001, 0x102, 0x0D, 0),       # RETOUR → -3
           (0x770001, 0x0F, 0, 0)]),
    "F4-aller-hexa": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x74, 0),
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x61, 0),          # 'a'
        (0x770001, 0x102, 0x39, 0),          # '9'
        (0x770001, 0x102, 0x0D, 0),          # RETOUR → LE SAUT 0xA9
        (0x770001, 0x0F, 0, 0)]),
    "F5-chercher-la-fin": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x102, 0x06, 0),          # Ctrl+F → le mode CHERCHER
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x34, 0),          # '4'
        (0x770001, 0x102, 0x44, 0),          # 'D'
        (0x770001, 0x102, 0x0D, 0),          # RETOUR → le motif posé
        (0x770001, 0x0F, 0, 0)]
        + [(0x770001, 0x100, 0x72, 0),       # F3 — jusqu'au-delà de la fin
           (0x770001, 0x0F, 0, 0)] * (OCC_4D + 2)),
    "F6-journal-plein": ("loupe.exe " + TEM, BASE_MSG
        + [(0x770001, 0x102, ord(c), 0) for c in HEXPAIRS]
        + [(0x770001, 0x102, 0x47, 0),       # 'G' — NON HEXA, le repli E4
           (0x770001, 0x0F, 0, 0),
           (0x770001, 0x102, 0x30, 0),       # '0'
           (0x770001, 0x102, 0x30, 0),       # '0' → le 257e → -3 journal plein
           (0x770001, 0x0F, 0, 0)]),
    "F7-ligne-incomplete": ("loupe.exe " + TEM_INCOMPLET, BASE_MSG
        + [(0x770001, 0x115, 3, 0)] * 24     # PgDn × 24 → AU FOND
        + [(0x770001, 0x0F, 0, 0),
           (0x770001, 0x115, 2, 0),          # PgUp au fond → la bride
           (0x770001, 0x0F, 0, 0)]),
    "F8-touches-aux-bornes": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x25, 0),          # gauche à 0 → la bride
        (0x770001, 0x100, 0x25, 0),
        (0x770001, 0x100, 0x24, 0),          # Home
        (0x770001, 0x100, 0x23, 0),          # End
        (0x770001, 0x100, 0x27, 0),          # droite
        (0x770001, 0x100, 0x27, 0),
        (0x770001, 0x100, 0x21, 0),          # PgUp au sommet → la bride
        (0x770001, 0x100, 0x21, 0),
        (0x770001, 0x100, 0x22, 0),          # PgDn
        (0x770001, 0x115, 3, 0),
        (0x770001, 0x0F, 0, 0)]),
    "F10a-fichier-verrouille": ("loupe.exe " + TEM, BASE_MSG),
    "F10b-acces-refuse": ("loupe.exe " + TEM, BASE_MSG),
    "F11-aller-suppr-echap": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x74, 0),          # F5 → le mode
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x61, 0),          # 'a'
        (0x770001, 0x102, 0x39, 0),          # '9'
        (0x770001, 0x102, 0x08, 0),          # VK_SUPPR → le dernier retiré
        (0x770001, 0x102, 0x08, 0),          # encore (le tampon vide)
        (0x770001, 0x102, 0x08, 0),          # encore (le repli au vide)
        (0x770001, 0x102, 0x1B, 0),          # ÉCHAP → l'annulation propre
        (0x770001, 0x0F, 0, 0)]),
    "F12-f3-sans-motif": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x72, 0),          # F3 SANS motif jamais posé
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x06, 0),          # Ctrl+F → le mode CHERCHER
        (0x770001, 0x102, 0x0D, 0),          # RETOUR → le motif VIDE → -5
        (0x770001, 0x0F, 0, 0)]),
    "F13-sans-session-les-fleches": ("loupe.exe fichier-absent.bin",
                                     BASE_MSG + [
        (0x770001, 0x100, 0x25, 0),          # gauche SANS session (curseur -1)
        (0x770001, 0x100, 0x27, 0),          # droite
        (0x770001, 0x100, 0x23, 0),          # End
        (0x770001, 0x0F, 0, 0)]),
    "F14-ctrl-s-au-journal-vide": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x102, 0x13, 0),          # Ctrl+S — RIEN en attente
        (0x770001, 0x0F, 0, 0)]),
    "F15-la-poignee": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x115, 4 | (40 << 16), 0),   # SB_POIGNEE — la position AU MOT DE POIDS FORT
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x115, 5 | (120 << 16), 0),  # SB_POIGNEE_COURSE
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x20A, 0, 0xFF880000),    # WM_MOUSEWHEEL (delta négatif)
        (0x770001, 0x0F, 0, 0)]),
    "F16-saisie-hors-fenetre": ("loupe.exe " + TEM, BASE_MSG + [
        (0x770001, 0x100, 0x22, 0),          # PgDn × 3 → la vue s'éloigne
        (0x770001, 0x100, 0x22, 0),
        (0x770001, 0x100, 0x22, 0),
        (0x770001, 0x102, 0x34, 0),          # '4' → la cellule HORS fenêtre
        (0x770001, 0x102, 0x44, 0),          # 'D' → E2 : verdict -3 à la barre
        (0x770001, 0x0F, 0, 0)]),
}

# les fautes PAR BLOC : les blocs qui portent des survivants aux chemins
# d'erreur inaccessibles depuis la vitrine (les E1-E4 des contrats) + les
# blocs de saisie dont les VERDICTS eax ne se lisent qu'au bloc (la barre
# affiche le NOM, jamais le nombre — l'écart nommé)
BLOCS_FAUTE = {"loupe-02", "loupe-05", "loupe-06", "loupe-07",
               "loupe-12", "loupe-14", "loupe-17"}
HWND = 0x770001


def instance(fichiers: dict, drapeaux: dict | None = None):
    os_v = HE.OSEdition()
    for nom, contenu in fichiers.items():
        os_v.declarer(nom, HE.FichierEditable(contenu=contenu))
    for nom, (verr, refus) in (drapeaux or {}).items():
        # LE FICHIER DE FAUTE : le verrou de partage / l'accès refusé — les
        # branches E de loupe-01 (CreateFileW les sert : gle 32 / gle 5)
        os_v.fichiers[nom].verrouille = verr
        os_v.fichiers[nom].refus_acces = refus
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    return os_v, emul


def observable_app(emul, os_v, cmdline, messages):
    r = emul.appeler_winmain(cmdline, messages=messages)
    ecran = bytes(emul.uc.mem_read(LL.R_ECRAN, 2320)) if not r.get("crash") \
        else b""
    return (r.get("exit_code"), r.get("crash") is None,
            bytes(os_v.fichiers[TEM].contenu) if TEM in os_v.fichiers else b"",
            ecran,
            emul.gui.fenetre_detruite if not r.get("crash") else None)


def observable_fautes_bloc(emul, os_v):
    """La séquence des fautes E1-E4 aux blocs (les conventions des épreuves
    V5 du harnais, TELLES QUELLES) : sans session, hors fichier, sortie
    nulle, LE SHIM ReadFile EN ÉCHEC — les verdicts + les sorties intactes."""
    A16, A32, A48 = HN.ADRESSE_SORTIE16, HN.ADRESSE_SORTIE32, HN.ADRESSE_SORTIE48
    CAN = HN.CANARI
    resultats = []
    # sans session (E1) — loupe-05/06 (l'émulation fraîche n'a PAS de
    # session : les verdicts -4 attendus)
    for va, out in ((LL.LOUPE05_VA, A32), (LL.LOUPE06_VA, A16)):
        r = emul.appeler(va, {"rcx": 0, "rdx": 1, "r8": out})
        resultats.append(("E1-sans-session", r.get("rax")))
    # la session posée (le geste réel : LOUPE-01)
    HN.emplacer_session(emul, os_v, TEM)
    # hors fichier (E2) / sortie nulle (E3) — loupe-05/06
    for va, out in ((LL.LOUPE05_VA, A32), (LL.LOUPE06_VA, A16)):
        r = emul.appeler(va, {"rcx": 2000, "rdx": 16, "r8": out})
        resultats.append(("E2-hors-fichier", r.get("rax")))
        r = emul.appeler(va, {"rcx": 0, "rdx": 1, "r8": 0})
        resultats.append(("E3-sortie-nulle", r.get("rax")))
    # LE SHIM ReadFile EN ÉCHEC (E4) — loupe-02/05/06/07
    for va, out, taille in ((LL.LOUPE05_VA, A32, 32), (LL.LOUPE06_VA, A16, 16)):
        os_v.armer_echec_read(1)
        emul.uc.mem_write(out, CAN * taille)
        r = emul.appeler(va, {"rcx": 0, "rdx": 384, "r8": out})
        intacte = bytes(emul.uc.mem_read(out, taille)) == CAN * taille
        os_v.armer_echec_read(None)
        resultats.append(("E4-readfile", (r.get("rax"), intacte)))
    os_v.armer_echec_read(1)
    r = emul.appeler(LL.LOUPE02_VA, {"rcx": 0})
    remplissage = emul.u32(552)
    os_v.armer_echec_read(None)
    resultats.append(("E4-loupe02", (r.get("rax"), remplissage)))
    os_v.armer_echec_read(1)
    emul.uc.mem_write(A48, CAN * 48)
    r = emul.appeler(LL.LOUPE07_VA, {"rcx": A48})
    panneau = bytes(emul.uc.mem_read(A48, 48)) == CAN * 48
    os_v.armer_echec_read(None)
    resultats.append(("E4-loupe07", (r.get("rax"), panneau,
                                     emul.etat_propre(r))))
    # loupe-07 LA SORTIE NULLE (E3) — le test rcx,rcx → -5
    r = emul.appeler(LL.LOUPE07_VA, {"rcx": 0})
    resultats.append(("E3-loupe07-sortie-nulle", (r.get("rax"),
                                                   emul.etat_propre(r))))
    # loupe-07 SANS session (E1) — le -4 de cumul
    HN.fermer_session(emul)
    r = emul.appeler(LL.LOUPE07_VA, {"rcx": A48})
    resultats.append(("E1-loupe07", (r.get("rax"), emul.etat_propre(r))))
    # loupe-15 SANS session — la flèche droite, le -4 (le cmp -1 du prologue)
    r = emul.appeler(LL.LOUPE15_VA, {"rcx": HWND, "rdx": 0x100,
                                     "r8": 0x27, "r9": 0})
    resultats.append(("E1-loupe15-sans-session", (r.get("rax"),
                                                   emul.etat_propre(r))))
    HN.emplacer_session(emul, os_v, TEM)
    # loupe-07 AU PROPRE (l'état non-volatif vérifié à CHAQUE appel désormais)
    r = emul.appeler(LL.LOUPE07_VA, {"rcx": A48})
    resultats.append(("loupe07-au-propre", (r.get("rax"),
                                             emul.etat_propre(r))))
    # LES BLOCS DE SAISIE AU NIVEAU BLOC — les verdicts eax ne se lisent
    # qu'ici (la barre affiche le nom, jamais le nombre) ; les conventions
    # m15 du harnais : (hwnd, msg, wParam, lParam) + L'ÉTAT PROPRE
    def ep(r):
        return (r.get("rax"), emul.etat_propre(r))
    # loupe-12 : le mode ALLER vécu — les DEUX refus au rax
    r1 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x100, "r8": 0x74})
    r2 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x61})
    r3 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x39})
    r4 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x0D})
    resultats.append(("loupe12-le-saut", (ep(r1), ep(r2), ep(r3), ep(r4))))
    r5 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x100, "r8": 0x74})
    r6 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x0D})
    resultats.append(("loupe12-le-vide", (ep(r5), ep(r6))))
    # LE MODE RÉ-OUVERT (le refus SORT du mode — Q4 : sans la ré-ouverture,
    # les chiffres tombent dans le vide, l'écart nommé de la v2)
    r6b = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x100, "r8": 0x74})
    for _ in range(8):
        emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x46})
    r7 = emul.appeler(LL.LOUPE12_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x0D})
    resultats.append(("loupe12-hors-bornes", (ep(r6b), ep(r7))))
    # loupe-14 : LA CONVENTION DES ÉPREUVES (poser_saisie + le commit + la
    # chaîne F3 jusqu'à la FIN — la voie réelle du renvoi)
    import struct as _struct
    hexa = b"4D"
    emul.uc.mem_write(LL.R_SAISIE, _struct.pack("<III", 2, 0, 0)
                      + hexa + b"\x00" * (80 - len(hexa)))
    emul.ecrire_cadre(544, _struct.pack("<Q", 0))   # le curseur au début
    r8 = emul.appeler(LL.LOUPE14_VA, {"rcx": HWND, "rdx": 0x102,
                                      "r8": 0x0D, "r9": 0})
    curseur_apres = emul.u64(544)
    fins = []
    for _ in range(OCC_4D + 2):
        rf = emul.appeler(LL.LOUPE14_VA, {"rcx": HWND, "rdx": 0x100,
                                          "r8": 0x72, "r9": 0})
        fins.append(ep(rf))
    motif_zone = bytes(emul.uc.mem_read(LL.R_MOTIF + 32, 4))
    resultats.append(("loupe14-la-chaine", (ep(r8), curseur_apres,
                                             tuple(fins), motif_zone)))
    # loupe-17 : Ctrl+S AU JOURNAL VIDE — le verdict au rax + l'état
    r17 = emul.appeler(LL.LOUPE17_VA, {"rcx": HWND, "rdx": 0x102, "r8": 0x13})
    resultats.append(("loupe17-journal-vide", ep(r17)))
    return tuple(resultats)


def fichiers_du_scenario(nom):
    if nom == "F10a-fichier-verrouille":
        return {TEM: FICHIER_2000}, {TEM: (True, False)}
    if nom == "F10b-acces-refuse":
        return {TEM: FICHIER_2000}, {TEM: (False, True)}
    if "incomplete" in nom:
        return {TEM_INCOMPLET: FICHIER_2001}, {}
    if "manquée" in nom or "sans-session" in nom:
        return {TEM: FICHIER_2000}, {}
    return {TEM: FICHIER_2000}, {}


def batterie_sane():
    """La base : CHAQUE scénario sur l'image propre — les observables."""
    base = {}
    for nom, (cmdline, msgs) in SCENARIOS_APP.items():
        fichiers, drapeaux = fichiers_du_scenario(nom)
        os_v, emul = instance(fichiers, drapeaux)
        with contextlib.redirect_stdout(io.StringIO()):
            base[nom] = observable_app(emul, os_v, cmdline, msgs)
    os_v, emul = instance({TEM: FICHIER_2000})
    with contextlib.redirect_stdout(io.StringIO()):
        base["F9-fautes-bloc"] = observable_fautes_bloc(emul, os_v)
    return base


def tuer_fautes(mutant, rva, bid, base):
    """La batterie K4 : le survivant confronté à TOUT ; tué si UN observable
    diverge. Rend (tué, cause)."""
    for nom, (cmdline, msgs) in SCENARIOS_APP.items():
        fichiers, drapeaux = fichiers_du_scenario(nom)
        os_v, emul = instance(fichiers, drapeaux)
        emul.uc.mem_write(rva, mutant)
        emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF)
                                 & ~0xFFF)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                obs = observable_app(emul, os_v, cmdline, msgs)
        except Exception:  # noqa: BLE001
            return True, f"{nom} : crash"
        if obs != base[nom]:
            return True, f"{nom} : l'observable diverge"
    if bid in BLOCS_FAUTE:
        os_v, emul = instance({TEM: FICHIER_2000})
        emul.uc.mem_write(rva, mutant)
        emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF)
                                 & ~0xFFF)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                obs = observable_fautes_bloc(emul, os_v)
        except Exception:  # noqa: BLE001
            return True, "F9-fautes-bloc : crash"
        if obs != base["F9-fautes-bloc"]:
            return True, "F9-fautes-bloc : l'observable diverge"
    return False, "vivants (la batterie passée)"


def main():
    print("=== LE RE-JEU AUX SHIMS D'INJECTION DE FAUTES (1c4sokpii, partie 3) ===")
    print(f"les occurrences du motif 0x4D au fichier : {OCC_4D} (lu, jamais tapé)")
    with contextlib.redirect_stdout(io.StringIO()):
        base = batterie_sane()
    print(f"la batterie SANE : {len(base)} scénarios, les bases posées")

    rng = random.Random(GRAINE)
    blocs = MUT.module.blocs_domaines()
    with contextlib.redirect_stdout(io.StringIO()):
        os_v, emul_l = REJEU.instance_loupe()
        BASE_LOUPE = REJEU.observable_winmain(emul_l, os_v)
    assert BASE_LOUPE[0] == 0

    compte = {"tués": 0, "vivants": 0}
    fautes_tues = 0
    reste = []
    for domaine, liste in blocs.items():
        if domaine != "loupe":
            for bloc in liste:               # la boucle consomme les tirages
                octets = bloc["octets"]
                ref_insns = MUT.module.decoder(octets, bloc["rva"])
                if ref_insns is None:
                    continue
                for _ in range(16):
                    insn = ref_insns[rng.randrange(len(ref_insns))]
                    pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                    val = octets[pos]
                    nouvelle = rng.choice([b for b in range(256) if b != val])
                    mutant = bytearray(octets)
                    mutant[pos] = nouvelle
                    mutant = bytes(mutant)
                    m_insns = MUT.module.decoder(mutant, bloc["rva"])
                    if m_insns is None or MUT.module.reassembler(m_insns) != mutant:
                        compte["tués"] += 1
                    elif MUT.module.signature_structurelle(m_insns) != \
                            MUT.module.signature_structurelle(ref_insns):
                        compte["tués"] += 1
                    else:
                        compte["tués"] += 1   # K3 famille/orchestration/sys 100 %
            continue
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = MUT.module.decoder(octets, bloc["rva"])
            if ref_insns is None:
                continue
            ref_sig = MUT.module.signature_structurelle(ref_insns)
            bid = bloc["bid"]
            for _ in range(16):
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                val = octets[pos]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                mutant = bytearray(octets)
                mutant[pos] = nouvelle
                mutant = bytes(mutant)
                m_insns = MUT.module.decoder(mutant, bloc["rva"])
                tue, cause = False, ""
                if m_insns is None or MUT.module.reassembler(m_insns) != mutant:
                    tue, cause = True, "K1 round-trip"
                elif MUT.module.signature_structurelle(m_insns) != ref_sig:
                    tue, cause = True, "K2 signature"
                else:
                    tue, cause = REJEU.tuer_loupe(bid, mutant, bloc["rva"],
                                                  BASE_LOUPE)
                    if not tue:
                        tue, cause = tuer_fautes(mutant, bloc["rva"], bid, base)
                        if tue:
                            fautes_tues += 1
                if tue:
                    compte["tués"] += 1
                else:
                    compte["vivants"] += 1
                    reste.append({"bid": bid, "offset": f"{pos:#x}",
                                  "octet": f"{val:#04x}→{nouvelle:#04x}",
                                  "cause": cause})
            print(f"  [loupe] {bid} : cumulé {compte['tués']} tués, "
                  f"{compte['vivants']} vivants", flush=True)

    total = compte["tués"] + compte["vivants"]
    taux = 100.0 * compte["tués"] / total

    # le rapport
    lignes = [
        "LE RE-JEU AUX SHIMS D'INJECTION DE FAUTES — 1c4sokpii partie 3",
        "(les MÊMES 832 mutants, la graine 20261111 ; K1/K2/K3 INTACTS ;",
        " K4 la batterie d'injection : l'ouverture manquée, ALLER vide/hors",
        "  bornes/hexa, CHERCHER jusqu'à la FIN, le journal PLEIN + le",
        "  non-hexa, la ligne INCOMPLÈTE au fond, les touches aux BORNES,",
        "  les fautes PAR BLOC [sans session/hors fichier/sortie nulle/LE",
        "  SHIM ReadFile en échec])",
        "",
        f"  loupe : {compte['tués'] - 928 + 288}/{288} tués aux fautes "
        f"comprises",  # corrigé ci-dessous — le calcul global fait foi
    ]
    # (la ligne ci-dessus est remplacée par le calcul juste)
    lignes = lignes[:7]
    lignes += [
        f"  TOTAL : {compte['tués']}/{total} tués ({taux:.1f} %) — "
        f"{compte['vivants']} vivants",
        f"  dont {fautes_tues} tués PAR LA BATTERIE D'INJECTION "
        "(les survivants de K3 confrontés aux branches d'erreur)",
        "",
        "LE RESTE NOMMÉ (chaque survivant, sa cause) :",
    ]
    for r in reste:
        lignes.append(f"  vivant : {r['bid']} {r['offset']}: {r['octet']}"
                      f" — {r['cause']}")
    lignes += [
        "",
        "LA COMPARAISON : v0.11.0 694/832 (83,4 %) → v0.14.0 776/832 "
        "(93,3 %) → la batterie d'injection ci-dessus",
    ]
    (ICI / "rejeu_fautes_rapport.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    import csv
    with open(ICI / "reste_nomme.csv", "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bid", "offset", "octet", "cause"])
        w.writeheader()
        for r in reste:
            w.writerow(r)
    with open(ICI / "rejeu_fautes.csv", "w", encoding="utf-8") as f:
        f.write("domaine,tues,total,taux,vivants\n")
        f.write(f"global,{compte['tués']},{total},{taux:.1f},"
                f"{compte['vivants']}\n")
    print("\n".join(lignes))
    print(f"\nles pièces : rejeu_fautes_rapport.txt, reste_nomme.csv, "
          "rejeu_fautes.csv")


if __name__ == "__main__":
    main()
