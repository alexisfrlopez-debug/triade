#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuzz.py — Fuzzing à propriétés du jalon M3 (ouverture, D45).

Le critère M3 — « un million de requêtes fuzzées sans crash » — exige un
harnais AVANT les blocs M3 (parseur HTTP à contrats renforcés). Ce harnais
calibre la méthodologie sur la surface d'entrées non fiables DÉJÀ scellée :

  - tcp-09 (c30009 @0x4800, session serveur M2) : la boucle recv/écho/send
    consomme des octets réseau NON FIABLES (longueur et contenu arbitraires) ;
  - win-10 (d40010 @0x4980, échange client démo) : la boucle de réception
    cumulative consomme la réponse du serveur — non fiable elle aussi.

Propriétés vérifiées PAR CAS (dérivées des contrats I, jamais au-delà) :
  P1 SURVIE   : aucune faute d'exécution (UcError = crash processus terrain) ;
  P2 TERMINAISON : le bloc rend la main dans le budget d'instructions ;
  P3 DIFFÉRENTIEL : l'écho émis == l'entrée reçue (tcp-09, v1 identité) ;
                   le verdict eax == le verdict calculé par le modèle (win-10) ;
  P4 FERMETURE : la socket cliente est fermée EXACTEMENT une fois (Q2 tcp-09) ;
  P5 MÉMOIRE   : aucune écriture hors zones légitimes — pages de code de
                 l'image (aucune, patch désactivé), pile sous la profondeur
                 maximale légitime (I4).

Architecture : lots de L cas par émutateur (l'état Unicorn est recréé toutes
les L itérations) ; tout échec est REJOUÉ sur émutateur vierge avant d'être
consigné (exclusion des artefacts de réutilisation) ; graine maîtresse →
scénario reproductible (générateurs nommés, déterministes par cas).

Usage :
  python3 fuzz.py --cible tcp-09 --cas 20000 --graine 1
  python3 fuzz.py --cible win-10 --cas 10000 --graine 2
  python3 fuzz.py --calibration            # 500 cas, verbosité maximale
"""

from __future__ import annotations

import argparse
import os
import random
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.join(os.path.dirname(ICI), "demo")
sys.path.insert(0, DEMO)

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("layout_demo", os.path.join(DEMO, "layout.py"))
L = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)
sys.modules["layout_demo"] = L

import oracle_demo as od           # émulateur + shims (D29/D36/D42)
from unicorn import UcError, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RSP

IMAGE = L.IMAGE_BASE
PILE = od.PILE_BASE
RVA_TCP09 = 0x4800                  # c30009 — session serveur scellée M2
RVA_WIN10 = 0x4980                  # d40010 — échange client scellé démo
SOCKET = 0x777
LIMITE_PILE = PILE + 0x7F000        # écriture sous ceci = violation (I4)
MAX_RECUS = 16                      # au plus 16 réceptions par scénario
TAILLE_TAMPON = 1024                # tampon tcp-09 (I2)


def installer_crochet_memoire(em):
    """Crochet d'écriture : P5 — pages de code image + pile profonde interdites.

    La pile légitime (cadres tcp-09 ~0x490 + appelés ~0x300) vit AU-DESSUS de
    LIMITE_PILE ; le crochet ne couvre que [PILE, LIMITE_PILE) et l'image
    [IMAGE, fin de .text2) — toute écriture y est une violation (le patch est
    désactivé : R_ETAT_PATCH = 0, aucun VirtualProtect n'a lieu).
    """
    etat = {"violation": None}

    def crochet(uc_, acces, adresse, taille, valeur, donnees):
        if etat["violation"] is not None:
            return
        if IMAGE <= adresse < IMAGE + L.DATA_RVA:
            etat["violation"] = f"écriture page de code @{adresse - IMAGE:#x}"
        elif PILE <= adresse < LIMITE_PILE:
            rsp = uc_.reg_read(UC_X86_REG_RSP)
            etat["violation"] = (f"écriture pile profonde @{adresse - PILE:#x} "
                                 f"(rsp courant {rsp - PILE:#x})")

    em.uc.hook_add(UC_HOOK_MEM_WRITE, crochet, begin=PILE, end=LIMITE_PILE - 1)
    em.uc.hook_add(UC_HOOK_MEM_WRITE, crochet,
                   begin=IMAGE, end=IMAGE + L.DATA_RVA - 1)
    return etat


# ---------------------------------------------------------------- générateurs

def gen_aleatoire(rng):
    """Octets uniformément aléatoires, longueurs aléatoires, fin aléatoire."""
    items = []
    for _ in range(rng.randint(1, MAX_RECUS)):
        n = rng.randint(0, TAILLE_TAMPON)
        items.append(bytes(rng.getrandbits(8) for _ in range(n)))
    items.append(rng.choice([0, -1]))
    return items


def gen_tronquatures(rng):
    """Préfixes croissants d'un flux mêlé (phrase, HTTP, octets 0-255)."""
    base = L.PHRASE + b"GET / HTTP/1.1\r\nHost: x\r\n\r\n" + bytes(range(256))
    items = []
    for _ in range(rng.randint(1, MAX_RECUS)):
        coupe = rng.randint(0, min(len(base), TAILLE_TAMPON))
        items.append(base[:coupe])
    items.append(rng.choice([0, -1]))
    return items


def gen_binaire_hostile(rng):
    """NUL, octets hauts, CRLF injectés, motifs de format, pleines capacités."""
    motifs = [b"\x00" * 64, b"\r\n" * 32, b"\xff" * 128, b"%s%s%n" * 16,
              b"\x80" + b"A" * 100, b"A" * TAILLE_TAMPON, b"\r\n\r\n",
              b"fin connexion", b"fin connexion\r\n", b"echo ", b"\x00\r\n\x00"]
    items = [rng.choice(motifs) for _ in range(rng.randint(1, MAX_RECUS))]
    items.append(rng.choice([0, -1]))
    return items


def gen_fragmentation(rng):
    """Découpe d'un flux hostile en fragments TCP réalistes (1-7 octets)."""
    flux = bytes(rng.getrandbits(8) for _ in range(rng.randint(8, 256)))
    items, i = [], 0
    while i < len(flux):
        pas = rng.randint(1, 7)
        items.append(flux[i:i + pas])
        i += pas
    items.append(rng.choice([0, -1]))
    return items


def gen_fins_prematurees(rng):
    """Réceptions vides ou en erreur, seules ou mêlées à des données."""
    items = []
    for _ in range(rng.randint(1, 6)):
        r = rng.random()
        if r < 0.4:
            items.append(rng.choice([0, -1]))
        elif r < 0.5:
            items.append(b"")
        else:
            items.append(bytes(rng.getrandbits(8)
                               for _ in range(rng.randint(1, 64))))
    items.append(rng.choice([0, -1]))
    return items


def gen_pleine_capacite(rng):
    """Réceptions aux frontières du tampon : 1023, 1024, 1025 octets."""
    items = []
    for _ in range(rng.randint(1, 4)):
        choix = rng.random()
        if choix < 0.34:
            items.append(bytes(rng.getrandbits(8) for _ in range(TAILLE_TAMPON)))
        elif choix < 0.67:
            items.append(bytes(rng.getrandbits(8) for _ in range(TAILLE_TAMPON - 1)))
        else:
            items.append(bytes(rng.getrandbits(8) for _ in range(TAILLE_TAMPON + 1)))
    items.append(rng.choice([0, -1]))
    return items


GENERATEURS = [
    ("aleatoire", gen_aleatoire),
    ("tronquatures", gen_tronquatures),
    ("binaire-hostile", gen_binaire_hostile),
    ("fragmentation", gen_fragmentation),
    ("fins-prematurees", gen_fins_prematurees),
    ("pleine-capacite", gen_pleine_capacite),
]


# ---------------------------------------------------------------- modèles

def attendu_tcp09(items):
    """Modèle de référence : l'écho v1 (identité) renvoie tout ce qui est reçu.

    Sémantique recv fidèle au contrat tcp-09/Q1-Q2 : le serveur ne demande
    JAMAIS plus que le tampon (cap 1024 — recv ne peut pas rendre davantage) ;
    un retour 0 (paire vide = fermeture du pair) ou ≤ 0 termine la session.
    (Ces deux règles étaient manquantes à la calibration : le harnais les a
    révélées comme divergences modèle/bloc — le bloc avait raison.)
    """
    emis = b""
    for it in items:
        if isinstance(it, int):
            assert it <= 0, "les générateurs ne scriptent que des fins (0, -1)"
            break                                  # Q2 : fin de session
        if not it:
            break                                  # recv = 0 : pair parti
        emis += it[:TAILLE_TAMPON]                 # recv borné par la demande
    return emis


def attendu_win10(items, phrase_attendue):
    """Modèle win-10 : accumulation jusqu'à 14 octets, memcmp exact.

    Chaque recv demande (14 - déjà reçus) — le serveur simulé ne sert que
    ce qui est demandé ; un retour vide/négatif termine en échec (E2).
    """
    acumul = b""
    for it in items:
        if isinstance(it, int):
            break
        if not it:
            break
        demande = 14 - len(acumul)
        acumul += it[:demande]
        if len(acumul) >= 14:
            break
    return 1 if acumul[:14] == phrase_attendue else 0


# ---------------------------------------------------------------- exécution

def jouer_tcp09(em, items):
    em.envois.clear()
    em.fermetures.clear()
    em.file_recv = list(items)
    return em.appeler(RVA_TCP09, (SOCKET,), limite=4_000_000)


def jouer_win10(em, items):
    em.envois.clear()
    em.fermetures.clear()
    em.file_recv = list(items)
    return em.appeler(RVA_WIN10, (SOCKET, IMAGE + L.R_PHRASE), limite=4_000_000)


def verifier_tcp09(items, r, em, etat_memoire):
    """P1-P4 contre le modèle (P1/P2 implicites : pas d'exception, retour rendu)."""
    fautes = []
    emis_reel = b"".join(em.envois)
    emis_modele = attendu_tcp09(items)
    if emis_reel != emis_modele:
        fautes.append(f"P3 écho divergent : {len(emis_reel)} o émis != "
                      f"{len(emis_modele)} o attendus")
    if len(em.fermetures) != 1 or em.fermetures[0] != SOCKET:
        fautes.append(f"P4 fermetures {em.fermetures!r} != exactement "
                      f"[{SOCKET:#x}] (Q2)")
    if etat_memoire["violation"]:
        fautes.append(f"P5 {etat_memoire['violation']}")
    return fautes


def verifier_win10(items, r, em, etat_memoire):
    fautes = []
    eax = r & 0xFFFFFFFF
    attendu = attendu_win10(items, L.PHRASE)
    if eax not in (0, 1):
        fautes.append(f"P3 verdict hors domaine : eax={eax:#x}")
    elif eax != attendu:
        fautes.append(f"P3 verdict divergent : eax={eax} != {attendu} "
                      f"(accumulation 14 + memcmp)")
    if em.envois and em.envois[0][:14] != L.PHRASE:
        fautes.append(f"P3 émission inattendue : {em.envois[0][:20]!r}")
    if etat_memoire["violation"]:
        fautes.append(f"P5 {etat_memoire['violation']}")
    return fautes


# ---------------------------------------------------------------- campagne

with open(os.path.join(DEMO, "demo.exe"), "rb") as _f:
    EXE = _f.read()

# sites de mutation pour l'auto-test (falsification du harnais lui-même :
# un oracle qui ne peut pas échouer ne prouve rien)
FILEOFF_TCP09_RECV = 0x341B + 3     # imm32 de « mov r8d, 0x400 » @0x481b (0x04)
FILEOFF_WIN10_MEMCMP = None        # calculé ci-dessous (imm de « mov r8d, 0xe »)
_m = EXE.find(bytes.fromhex("41b80e000000"), 0x2C00 + (0x4980 - 0x4000))
if 0 <= _m <= 0x2C00 + (0x4980 - 0x4000) + 0x180:
    FILEOFF_WIN10_MEMCMP = _m + 2  # octet de poids faible de l'imm32 (0x0e = 14)


def auto_test():
    """Falsification du harnais : un défaut injecté DOIT être détecté.

    tcp-09 : la demande recv passe de 1024 à 768 octets (un octet) — l'écho
    tronque les réceptions pleines capacité : P3 doit fauter. win-10 : la
    longueur memcmp passe de 14 à 13 (un octet) — le verdict 1 est rendu sur
    des entrées divergeant au 14e octet : P3 doit fauter. Un harnais qui ne
    détecte NI l'un NI l'autre ne vérifie rien (miroir des falsifications
    V4-V9 de l'oracle démo).
    """
    print("=== auto-test : falsification du harnais (défauts injectés) ===")
    ok = True
    # 1. tcp-09 muté : recv 1024 -> 768
    mutant = bytearray(EXE)
    assert mutant[FILEOFF_TCP09_RECV] == 0x04, "site recv tcp-09 divergent"
    mutant[FILEOFF_TCP09_RECV] = 0x03
    b = campagne("tcp-09", 300, graine=99, verbeux=False, exe=bytes(mutant))
    detecte = len(b["echecs"]) > 0 and any(
        "P3" in f for e in b["echecs"] for f in e["fautes"])
    print(f"  [1] tcp-09 recv 0x400->0x300 : {len(b['echecs'])} échec(s) "
          f"confirmé(s) — {'DÉTECTÉ' if detecte else 'NON DÉTECTÉ !'}")
    ok &= detecte
    # 2. win-10 muté : memcmp 14 -> 13
    if FILEOFF_WIN10_MEMCMP is not None:
        mutant = bytearray(EXE)
        assert mutant[FILEOFF_WIN10_MEMCMP] == 0x0E, "site memcmp win-10 divergent"
        mutant[FILEOFF_WIN10_MEMCMP] = 0x0D
        b = campagne("win-10", 300, graine=99, verbeux=False, exe=bytes(mutant))
        detecte = len(b["echecs"]) > 0 and any(
            "P3" in f for e in b["echecs"] for f in e["fautes"])
        print(f"  [2] win-10 memcmp 14->13 : {len(b['echecs'])} échec(s) "
              f"confirmé(s) — {'DÉTECTÉ' if detecte else 'NON DÉTECTÉ !'}")
        ok &= detecte
    else:
        print("  [2] site memcmp win-10 introuvable — ABSENT !")
        ok = False
    print(f"AUTO-TEST : {'PASS — le harnais détecte les défauts injectés' if ok else 'ÉCHEC — harnais aveugle !'}")
    return 0 if ok else 1


def nouvel_emulateur(artefact=None):
    em = od.Emulateur(artefact if artefact is not None else EXE)
    em.installer_shims()
    em.cs_init.add(IMAGE + L.R_CS)                       # P2 tcp-09 (D42)
    em.uc.mem_write(IMAGE + L.R_STDOUT, struct.pack("<Q", od.FAKE_STDOUT))
    em.uc.mem_write(IMAGE + L.R_STDIN, struct.pack("<Q", od.FAKE_STDOUT))
    etat = installer_crochet_memoire(em)
    return em, etat


def campagne(cible, nb_cas, graine, taille_lot=50, verbeux=False, exe=None):
    rng = random.Random(graine)
    echecs, executes = [], 0
    em = etat = None
    debut = time.time()
    artefact = exe if exe is not None else EXE

    for i in range(nb_cas):
        if em is None or i % taille_lot == 0:
            em, etat = nouvel_emulateur(artefact)
        nom_gen, gen = GENERATEURS[i % len(GENERATEURS)]
        items = gen(rng)
        etat["violation"] = None
        try:
            if cible == "tcp-09":
                r = jouer_tcp09(em, items)
                fautes = verifier_tcp09(items, r, em, etat)
            else:
                r = jouer_win10(em, items)
                fautes = verifier_win10(items, r, em, etat)
        except (UcError, od.EchecOracle) as exc:
            fautes = [f"P1 faute d'exécution : {exc}"]
        if fautes:
            # rejeu sur émutateur VIERGE : exclut tout artefact de réutilisation
            em2, etat2 = nouvel_emulateur(artefact)
            confirme = []
            try:
                if cible == "tcp-09":
                    r2 = jouer_tcp09(em2, items)
                    confirme = verifier_tcp09(items, r2, em2, etat2)
                else:
                    r2 = jouer_win10(em2, items)
                    confirme = verifier_win10(items, r2, em2, etat2)
            except (UcError, od.EchecOracle) as exc:
                confirme = [f"P1 faute d'exécution (rejeu) : {exc}"]
            if confirme:
                echecs.append({"cas": i, "generateur": nom_gen,
                               "items": items, "fautes": confirme})
                print(f"[ÉCHEC confirmé] cas {i} ({nom_gen}) : {confirme}")
        executes += 1
        if verbeux and i % 100 == 0 and i:
            print(f"  … {i} cas, {time.time() - debut:.0f}s, "
                  f"{len(echecs)} échec(s)")

    return {"executes": executes, "echecs": echecs,
            "duree": time.time() - debut, "graine": graine, "cible": cible}


def formater_items(items, limite=3):
    out = []
    for it in items[:limite]:
        if isinstance(it, int):
            out.append(f"retour({it})")
        else:
            out.append(f"{len(it)}o:{it[:24]!r}{'…' if len(it) > 24 else ''}")
    return out


def main():
    ap = argparse.ArgumentParser(description="Fuzzing à propriétés M3 (ouverture)")
    ap.add_argument("--cible", choices=("tcp-09", "win-10"), default="tcp-09")
    ap.add_argument("--cas", type=int, default=10_000)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--lot", type=int, default=50)
    ap.add_argument("--calibration", action="store_true")
    ap.add_argument("--auto-test", action="store_true",
                    help="falsification : défauts injectés, le harnais DOIT détecter")
    ap.add_argument("--verbeux", action="store_true")
    args = ap.parse_args()
    if args.auto_test:
        return auto_test()
    if args.calibration:
        args.cas, args.verbeux = 500, True

    print(f"=== M3 fuzz à propriétés — cible {args.cible}, {args.cas} cas, "
          f"graine {args.graine} ===")
    print("    artefact : demo.exe (tcp-09/win-10 scellés, octet-identiques M2)")
    print(f"    générateurs : {', '.join(n for n, _ in GENERATEURS)}")
    bilan = campagne(args.cible, args.cas, args.graine, args.lot, args.verbeux)

    print("=" * 66)
    print(f"BILAN {bilan['cible']} : {bilan['executes']} cas en "
          f"{bilan['duree']:.1f}s "
          f"({bilan['executes'] / max(bilan['duree'], 0.001):.0f} cas/s)")
    print(f"  échecs confirmés (rejeu sur état vierge) : {len(bilan['echecs'])}")
    for e in bilan["echecs"][:10]:
        print(f"  - cas {e['cas']} [{e['generateur']}] : {e['fautes']}")
        print(f"    scénario : {formater_items(e['items'])}")
    verdict = ("SANS CRASH — propriétés P1-P5 tenues sur toute la campagne"
               if not bilan["echecs"]
               else f"{len(bilan['echecs'])} VIOLATION(S) DE CONTRAT")
    print(f"VERDICT : {verdict}")
    return 1 if bilan["echecs"] else 0


if __name__ == "__main__":
    sys.exit(main())
