#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite02.py — LE TERRAIN DE L'UNITÉ 2 (loupe-02 lire × bras T, la
campagne de comparaison des workflows D204).

RÉVISION v2 (14/11/2026, l'Entrée 294 — L'ÉCART DU JUGE NOMMÉ) : le run
terrain de la v1 (16:46:34Z, 18 VERT 2 ROUGE) révéla que le présent
scénario posait le journal à R_JOURNAL = 0xE4E0 — SOIXANTE-QUATRE octets
au-dessus de la vérité du layout (loupe/layout.py : R_JOURNAL = 0xE4A0,
l'adresse même que le lea de la pièce vise, lue à l'octet près au
scripts/campagne_d204/depot-runs-kit-02-294/99_preuve_lea_exe.py). LA
PIÈCE ÉTAIT DROITE : le compte qu'elle lisait tombait à l'entrée #156 de
la zone zéroée du juge → compte 0 → AUCUN recouvrement → les DEUX
vecteurs V2 ROUGE (les-bords-de-fenetre, cinq-entrees-dont-une-non-
alignee) — rejoués octet par octet au labo (100_epreuves_juge.py). LE
SEUL CHANGEMENT de la v2 : la constante remise à la vérité du layout
(0xE4A0) ; la pièce et les HUIT autres pièces du kit demeurent INTACTES
octet pour octet celles de la v1 (D143 : le kit v1 demeure au coffre).

Le kit porte UNE pièce et UN scénario :
  loupe.exe          la pièce de campagne — le build du plan où le slot
                     loupe-02 (RVA 0x4240) porte LA NOTATION DE CAMPAGNE
                     écrite à la main par l'agent (292 o, 79 instructions —
                     le contrat loupe-02:R1 : la fenêtre bornée + LE
                     RECOUVREMENT du journal) ; les dix-sept autres blocs
                     demeurent les SCELLÉS du projet — loupe-01 scellé
                     APPELLE la notation de campagne à chaque naissance de
                     session (la fenêtre à la vue 0) ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, struct,
                     sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé) : le
scénario est LE CHARGEUR — LoadLibraryEx DONT_RESOLVE (aucune entrée
résolue, AUCUN point d'entrée exécuté), il résout LUI-MÊME les SIX feuilles
kernel32 du noyau aux slots du plan (VirtualProtect sur .rdata le temps du
geste), ouvre la session PAR LOUPE-01 SCELLÉ (la session née entière — la
première fenêtre naît de la notation de campagne), et APPELLE LOUPE-02 À
SON ADRESSE AU PLAN (base + 0x4240), conduite par la main du kit. Le juge
est le MODÈLE INDÉPENDANT (hashlib, les découpes) — jamais les octets du
bloc.

LES VECTEURS DU CONTRAT (loupe-02 révision 1) :
  V1  le différentiel : les témoins du kit — temoin-1.bin (1 o),
      temoin-384.bin (384 o), temoin-3f.bin (3 × 64 Kio + 1) — la fenêtre
      née à l'ouverture (loupe-01 scellé a appelé la notation de campagne),
      puis les décalages : les frontières (0, la dernière pleine, la
      dernière partielle) + la graine fixe (100 tirés) — le tampon == la
      découpe, remplissage == min(384, taille − décalage), la vue et le
      curseur INTACTS ; le vide s'ouvre SANS fenêtre, aucun décalage n'y
      est valide ;
  V2  le recouvrement du journal : les entrées posées aux BORDS de la
      fenêtre (le premier, le dernier, l'avant, l'après) puis CINQ dedans
      dont une NON ALIGNÉE — l'octet écrit REMPLACE l'octet lu, l'édition
      survit au défilement ; le journal INTACT après le geste ;
  V3  les rejets : sans session → -4 ; décalage non multiple de 16 → -5 ;
      à la taille exacte et au-delà → -3 — RIEN lu : le tampon empoisonné
      et le remplissement INTACTS ;
  V4  l'échec système : la plage [0, 384) VERROUILLÉE par un second
      détenteur (LockFile) → ReadFile refuse → -6, remplissage 0
      (fail-closed), la session SURVIT (la lecture suivante verte) ; si le
      verrou de plage ne fait pas échouer la lecture au terrain :
      NOMMÉ ABSENT, jamais maquillé ;
  V5  la falsification demandée : un octet du tampon muté après lecture —
      l'état lu DIVERGE du modèle (le juge lit l'état).

  le témoin : temoin-unite02.txt au réceptacle preuves-unite02/ —
  DATER ET SIGNER DE VOTRE MAIN (jamais automatisé, D99), renvoyer le
  dossier ENTIER au coffre /test.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import random
import struct
import sys
import datetime as dt

ICI = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ICI, "loupe.exe")
RECEPTACLE = os.path.join(ICI, "preuves-unite02")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
R_LOUPE01 = 0x4080
R_LOUPE02 = 0x4240
R_LOUPE03 = 0x4380
R_CADRE = 0xE000
R_JOURNAL = 0xE4A0            # loupe-16 : la vérité du layout (D161) ; la v1
                               # portait 0xE4E0 (+0x40) — l'écart du juge,
                               # nommé à l'Entrée 294
IAT_SLOTS = {"CreateFileW": 0x3118, "GetFileSizeEx": 0x3120,
             "SetFilePointerEx": 0x3128, "ReadFile": 0x3130,
             "CloseHandle": 0x3140, "GetLastError": 0x3148}
TAILLE, POIGNEE = 520, 528
VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568
ZONE_JOURNAL = 4112
GRAINE = 20261114

REUSSITES, ECARTS = [], []


def consigne(ligne: str) -> None:
    print(ligne, flush=True)


def verdict(rax: int) -> int:
    v = rax & 0xFFFFFFFF
    return v - 0x100000000 if v > 0x7FFFFFFF else v


def controle(nom: str, ok: bool, detail: str = "") -> None:
    consigne(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
             + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


def lire_empreintes() -> dict:
    empreintes = {}
    for fich in sorted(os.listdir(ICI)):
        if fich.startswith("EMPREINTES") and fich.endswith(".txt"):
            for ligne in open(os.path.join(ICI, fich), encoding="utf-8",
                              errors="replace").read().splitlines():
                parts = ligne.strip().split(None, 2)
                if len(parts) >= 2 and len(parts[0]) == 64:
                    empreintes[parts[1]] = parts[0].lower()
    return empreintes


def sha256_fichier(chemin: str) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for morceau in iter(lambda: f.read(1 << 20), b""):
            h.update(morceau)
    return h.hexdigest()


def decales_terrain(taille: int) -> list[int]:
    """Les décalages du terrain : les frontières à la main + la graine fixe
    (100 tirés pour les grands témoins — le terrain lit de vrais octets)."""
    rng = random.Random(GRAINE)
    out = [0]
    if taille >= 16:
        dernier = (taille - 1) // 16 * 16    # la dernière valide
        if dernier not in out:
            out.append(dernier)
        pleine = taille - 384                        # la dernière PLEINE
        if pleine >= 0:
            pleine -= pleine % 16
            if pleine >= 0 and pleine not in out:
                out.append(pleine)
        if taille % 16 == 0 and taille - 16 not in out:
            out.append(taille - 16)
        pool = list(range(0, (taille + 15) // 16 * 16, 16))
        out += [d for d in rng.sample(pool, min(100, len(pool)))
                if d not in set(out)]
    return out


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 2 (loupe-02 lire × bras T) — la campagne "
             "D204, le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_exe = sha256_fichier(EXE)
    attendu = empreintes.get("loupe.exe", "")
    if sha_exe != attendu:
        consigne(f"[T0] REFUS : loupe.exe {sha_exe[:16]}… != l'empreinte "
                 f"gravée {attendu[:16]}… — la pièce a divergé, rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe.exe sha256 {sha_exe[:16]}… == la gravure du kit")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]
    k32.GetProcAddress.restype = ctypes.c_void_p
    k32.GetProcAddress.argtypes = [ctypes.c_void_p, wt.LPCSTR]
    k32.GetModuleHandleW.restype = ctypes.c_void_p
    k32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
    k32.CreateFileW.restype = ctypes.c_void_p
    k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p]
    k32.LockFile.restype = wt.BOOL
    k32.LockFile.argtypes = [ctypes.c_void_p, wt.DWORD, wt.DWORD,
                             wt.DWORD, wt.DWORD]
    k32.UnlockFile.restype = wt.BOOL
    k32.UnlockFile.argtypes = [ctypes.c_void_p, wt.DWORD, wt.DWORD,
                               wt.DWORD, wt.DWORD]

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(EXE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")

    # LA RÉSOLUTION DES SIX FEUILLES DU NOYAU (le scénario est le chargeur)
    h_k32 = ctypes.c_void_p(k32.GetModuleHandleW("kernel32.dll"))
    ancien = wt.DWORD(0)
    zone_iat = base + 0x3000
    if not k32.VirtualProtect(ctypes.c_void_p(zone_iat), 0x300,
                              0x40, ctypes.byref(ancien)):
        consigne("[T0] REFUS : VirtualProtect sur l'IAT impossible")
        return 2
    for feuille, rva in IAT_SLOTS.items():
        adresse = k32.GetProcAddress(h_k32, feuille.encode("ascii"))
        if not adresse:
            consigne(f"[T0] REFUS : {feuille} introuvable à kernel32")
            return 2
        ctypes.memmove(base + rva, struct.pack("<Q", adresse), 8)
    k32.VirtualProtect(ctypes.c_void_p(zone_iat), 0x300, ancien.value,
                       ctypes.byref(ancien))
    consigne("[T0] les SIX feuilles du noyau résolues aux slots du plan "
             "(CreateFileW, GetFileSizeEx, SetFilePointerEx, ReadFile, "
             "CloseHandle, GetLastError)")

    # LES BLOCS COMME FONCTIONS (la conduite de la main du kit)
    LOUPE01 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(base + R_LOUPE01)
    LOUPE02 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64)(base + R_LOUPE02)
    LOUPE03 = ctypes.CFUNCTYPE(ctypes.c_int64)(base + R_LOUPE03)

    def appeler_ouvrir(tampon: bytes) -> int:
        zone = ctypes.create_string_buffer(bytes(tampon), len(tampon) + 8)
        r = LOUPE01(ctypes.cast(zone, ctypes.c_void_p))
        return verdict(r)

    def lire_fenetre(decalage: int) -> int:
        return verdict(LOUPE02(decalage))

    def ecrire_cadre(off: int, donnees: bytes) -> None:
        ctypes.memmove(base + R_CADRE + off, donnees, len(donnees))

    def cadre_champ(off: int, n: int = 8) -> bytes:
        brut = (ctypes.c_ubyte * n)()
        ctypes.memmove(brut, base + R_CADRE + off, n)
        return bytes(brut)

    def cadre_qword(off: int) -> int:
        return struct.unpack("<Q", cadre_champ(off, 8))[0]

    def cadre_dword(off: int) -> int:
        return struct.unpack("<I", cadre_champ(off, 4))[0]

    def poser_journal(entrees) -> None:
        brut = bytearray(ZONE_JOURNAL)
        for i, (dec, octet) in enumerate(entrees):
            brut[16 * i:16 * i + 16] = struct.pack("<QB7x", dec, octet)
        brut[4096:4100] = struct.pack("<I", len(entrees))
        ctypes.memmove(base + R_JOURNAL, bytes(brut), ZONE_JOURNAL)

    def journal_zone() -> bytes:
        brut = (ctypes.c_ubyte * ZONE_JOURNAL)()
        ctypes.memmove(brut, base + R_JOURNAL, ZONE_JOURNAL)
        return bytes(brut)

    def modele_tampon(donnees: bytes, decalage: int, journal):
        rempl = min(384, len(donnees) - decalage)
        tampon = bytearray(donnees[decalage:decalage + rempl])
        for dec, octet in journal:
            if decalage <= dec < decalage + rempl:
                tampon[dec - decalage] = octet
        return rempl, bytes(tampon)

    # ---- V1 : LE DIFFÉRENTIEL — la fenêtre bornée -----------------------------
    for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin"):
        donnees = open(os.path.join(ICI, nom), "rb").read()
        r = appeler_ouvrir(nom.encode("utf-16-le") + b"\x00\x00")
        rempl0 = min(384, len(donnees))
        controle(f"V1:{nom}-la-fenetre-nee-a-l-ouverture",
                 r == 0 and cadre_dword(REMPL) == rempl0
                 and cadre_champ(TAMPON, rempl0) == donnees[:rempl0],
                 f"loupe-01 scellé a appelé la notation de campagne : "
                 f"remplissage {cadre_dword(REMPL)} == min(384, {len(donnees)}), "
                 f"le tampon == la découpe")
        tout_ok, appels = True, 0
        for dec in decales_terrain(len(donnees)):
            avant_vue, avant_cur = cadre_qword(VUE), cadre_qword(CURSEUR)
            r = lire_fenetre(dec)
            rempl_att, tamp_att = modele_tampon(donnees, dec, [])
            tout_ok &= (r == 0 and cadre_dword(REMPL) == rempl_att
                        and cadre_champ(TAMPON, rempl_att) == tamp_att
                        and cadre_qword(VUE) == avant_vue
                        and cadre_qword(CURSEUR) == avant_cur)
            appels += 1
        controle(f"V1:{nom}-la-fenetre-bornee-a-{appels}-decalages", tout_ok,
                 f"{appels} décalages valides (les frontières + la graine "
                 f"{GRAINE}) : le tampon == la découpe, remplissage == "
                 f"min(384, taille − décalage), la vue et le curseur INTACTS")
        LOUPE03()
    # le vide : l'ouverture SANS fenêtre, AUCUN décalage valide
    donnees = open(os.path.join(ICI, "vide.bin"), "rb").read()
    r = appeler_ouvrir("vide.bin".encode("utf-16-le") + b"\x00\x00")
    controle("V1:vide.bin-l-ouverture-sans-fenetre",
             r == 0 and cadre_dword(REMPL) == 0,
             "le vide s'ouvre sans fenêtre (loupe-01 saute l'appelé) — "
             "remplissage 0")
    r = lire_fenetre(0)
    controle("V1:vide.bin-aucune-fenetre-valide", r == -3,
             f"rax={r} (sur le vide, décalage 0 ≥ taille 0 → -3 HORS-BORNES)")
    LOUPE03()
    # la vue pré-posée (Q3 renforcé) : la lecture ne déplace rien
    donnees = open(os.path.join(ICI, "temoin-3f.bin"), "rb").read()
    appeler_ouvrir("temoin-3f.bin".encode("utf-16-le") + b"\x00\x00")
    ecrire_cadre(VUE, (64).to_bytes(8, "little"))
    ecrire_cadre(CURSEUR, (65).to_bytes(8, "little"))
    r = lire_fenetre(4096)
    controle("V1:la-vue-et-le-curseur-intacts",
             r == 0 and cadre_qword(VUE) == 64 and cadre_qword(CURSEUR) == 65,
             "la lecture à 4096 ne déplace NI la vue (64) NI le curseur (65) "
             "— le défilement est à loupe-11")
    LOUPE03()

    # ---- V2 : LE RECOUVREMENT DU JOURNAL ---------------------------------------
    donnees = open(os.path.join(ICI, "temoin-3f.bin"), "rb").read()
    appeler_ouvrir("temoin-3f.bin".encode("utf-16-le") + b"\x00\x00")
    fen = 65536
    journal_bords = [(fen, 0xAA), (fen + 383, 0xBB),
                     (fen + 384, 0xCC), (fen - 16, 0xDD)]
    poser_journal(journal_bords)
    journal_avant = journal_zone()
    r = lire_fenetre(fen)
    rempl_att, tamp_att = modele_tampon(donnees, fen, journal_bords)
    controle("V2:les-bords-de-fenetre",
             r == 0 and cadre_dword(REMPL) == rempl_att
             and cadre_champ(TAMPON, rempl_att) == tamp_att,
             "le premier (0xAA) et le dernier (0xBB) recouverts ; l'avant "
             "(fenêtre−16) et l'après (fenêtre+384) IGNORÉS — l'édition "
             "survit au défilement")
    controle("V2:le-journal-intact", journal_zone() == journal_avant,
             "loupe-02 n'écrit JAMAIS au journal (I2 : la lecture ne touche "
             "que le tampon du cadre)")
    journal_multi = [(fen + 5, 0x11), (fen + 100, 0x22), (fen + 200, 0x33),
                     (fen + 300, 0x44), (fen + 383, 0x55)]
    poser_journal(journal_multi)
    r = lire_fenetre(fen)
    rempl_att, tamp_att = modele_tampon(donnees, fen, journal_multi)
    controle("V2:cinq-entrees-dont-une-non-alignee",
             r == 0 and cadre_champ(TAMPON, rempl_att) == tamp_att,
             "cinq entrées dedans (fen+5 NON ALIGNÉE comprise) — le tampon "
             "== le modèle indépendant")
    poser_journal([])
    LOUPE03()

    # ---- V3 : LES REJETS — rien lu, le tampon empoisonné INTACT ----------------
    r = lire_fenetre(0)
    controle("V3:E1-sans-session", r == -4,
             f"rax={r} (attendu -4 SESSION, la session fermée — rien lu)")
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    ecrire_cadre(TAMPON, b"\xCC" * 384)             # le poison
    ecrire_cadre(REMPL, (0xBEEF).to_bytes(4, "little"))
    poison, rempl_poison = cadre_champ(TAMPON, 384), cadre_dword(REMPL)
    r = lire_fenetre(40)
    controle("V3:E2-le-decalage-non-aligne",
             r == -5 and cadre_champ(TAMPON, 384) == poison
             and cadre_dword(REMPL) == rempl_poison,
             f"rax={r} (40 non multiple de 16 → -5 ENTRÉE), le tampon ET le "
             f"remplissage INTACTS (rien lu)")
    r = lire_fenetre(384)
    controle("V3:E3a-le-decalage-a-la-taille",
             r == -3 and cadre_champ(TAMPON, 384) == poison,
             f"rax={r} (384 == la taille → -3 HORS-BORNES), rien lu")
    r = lire_fenetre(1 << 40)
    controle("V3:E3b-le-decalage-immense",
             r == -3 and cadre_champ(TAMPON, 384) == poison,
             f"rax={r} (2^40 → -3 HORS-BORNES), rien lu")

    # ---- V4 : L'ÉCHEC SYSTÈME — la plage verrouillée par un second détenteur --
    verrou = k32.CreateFileW(os.path.join(ICI, "temoin-384.bin"),
                             0x80000000, 3, None, 3, 0, None)
    arme = bool(verrou) and bool(k32.LockFile(
        ctypes.c_void_p(verrou), 0, 0, 384, 0))
    if arme:
        r = lire_fenetre(0)
        if r == -6:
            controle("V4:la-plage-verrouillee",
                     r == -6 and cadre_dword(REMPL) == 0,
                     f"rax={r} (ReadFile refuse la plage verrouillée → -6 "
                     f"SYSTÈME), remplissage {cadre_dword(REMPL)} == 0 "
                     f"(fail-closed : jamais un octet non lu)")
        else:
            controle("V4:la-plage-verrouillee-NOMMÉ-ABSENT", True,
                     f"rax={r} — le verrou de plage n'a pas fait échouer la "
                     f"lecture au terrain (le système de fichiers l'ignore) "
                     f"— NOMMÉ ABSENT, jamais maquillé")
        k32.UnlockFile(ctypes.c_void_p(verrou), 0, 0, 384, 0)
        k32.CloseHandle(ctypes.c_void_p(verrou))
        r = lire_fenetre(0)
        controle("V4:la-session-survit",
                 r == 0 and cadre_dword(REMPL) == 384,
                 f"rax={r} — l'échec ne clôt PAS la session : la lecture "
                 f"suivante est verte, remplissage {cadre_dword(REMPL)}")
    else:
        if verrou:
            k32.CloseHandle(ctypes.c_void_p(verrou))
        controle("V4:la-plage-verrouillee-NOMMÉ-ABSENT", True,
                 "le verrou de plage n'a pu être posé au terrain — NOMMÉ "
                 "ABSENT, jamais maquillé")
    LOUPE03()

    # ---- V5 : LA FALSIFICATION DEMANDÉE (charte § 3) ---------------------------
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    r = lire_fenetre(0)
    donnees384 = open(os.path.join(ICI, "temoin-384.bin"), "rb").read()
    modele = donnees384[:384]
    ok_lecture = (r == 0 and cadre_champ(TAMPON, 384) == modele)
    octet_avant = cadre_champ(TAMPON, 384)[3]
    ecrire_cadre(TAMPON + 3, b"\xFF")                # l'octet muté
    divergence = cadre_champ(TAMPON, 384) != modele
    controle("V5:l-octet-mute-l-etat-lu-diverge",
             ok_lecture and divergence,
             f"la lecture d'abord VERT (le tampon == le modèle), l'octet 3 "
             f"muté {octet_avant:#04x} → 0xff : l'état lu DIVERGE du modèle "
             f"— la falsification est DÉTECTABLE (le juge lit l'état)")
    LOUPE03()

    # ---- LE TÉMOIN ---------------------------------------------------------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 2 — loupe-02 lire × bras T "
                  "(la campagne D204, la comparaison des workflows)")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe.exe {os.path.getsize(EXE)} o, "
                  f"sha256 {sha_exe}")
    lignes.append(f"le verdict  : {len(REUSSITES)} VERT, {len(ECARTS)} ROUGE "
                  f"{'— VERT' if not ECARTS else '— ÉCART NOMMÉ'}")
    lignes.append("")
    lignes.append("LES VECTEURS :")
    for nom in REUSSITES:
        lignes.append(f"  VERT {nom}")
    for nom in ECARTS:
        lignes.append(f"  ROUGE {nom}")
    lignes.append("")
    lignes.append("LE GESTE QUI RESTE À LA MAIN (jamais automatisé, D99) :")
    lignes.append("  DATER ce témoin (la date de votre main), le SIGNER,")
    lignes.append("  renvoyer le dossier preuves-unite02/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite02.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 2 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite02/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
