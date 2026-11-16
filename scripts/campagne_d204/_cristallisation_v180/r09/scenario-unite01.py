#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite01.py — LE TERRAIN DE L'UNITÉ 1 (loupe-01 × bras T, la
campagne de comparaison des workflows D204).

Le kit porte UNE pièce et UN scénario :
  loupe.exe          la pièce de campagne — le build du plan où le slot
                     loupe-01 (RVA 0x4080) porte LA NOTATION DE CAMPAGNE
                     écrite à la main par l'agent (sept éditions, six
                     correctifs comptés) ; les dix-sept autres blocs et
                     les huit héritages demeurent les SCELLÉS du projet —
                     la session née ENTIÈRE exige ses appelés ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, struct,
                     sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé) : le
scénario est LE CHARGEUR — LoadLibraryEx DONT_RESOLVE (aucune entrée
résolue, AUCUN point d'entrée exécuté), il résout LUI-MÊME les SIX
feuilles kernel32 du noyau aux slots du plan (VirtualProtect sur
.rdata le temps du geste) et APPELLE LOUPE-01 À SON ADRESSE AU PLAN
(base + 0x4080), conduite par la main du kit. Le juge est le MODÈLE
INDÉPENDANT (hashlib, les découpes) — jamais les octets du bloc.

LES VECTEURS DU CONTRAT (loupe-01 révision 3) :
  V1  les témoins du kit ouverts : temoin-1.bin (1 o), temoin-384.bin
      (384 o), temoin-3f.bin (3 × 64 Kio + 1), vide.bin (le vide de la
      révision 3) — le cadre lu champ à champ (chemin, taille, vue 0,
      curseur 0, remplissage min(384, taille)), le tampon == la découpe,
      le panneau 48 o == (md5, sha256) hashlib du fichier ENTIER ;
  V2  les rejets d'OS : absent → -2, verrouillé → -7 (le scénario tient
      le fichier sans partage) ; l'accès refusé ne s'arme pas proprement
      au terrain — NOMMÉ ABSENT du run, jamais maquillé ;
  V3  les bornes : la taille 2 Gio + 1 (un fichier réel posé à cette
      taille, épars) → -3 la poignée fermée ; la session double → -5
      l'ancien cadre INTACT ; le chemin de 260 caractères sans NUL → un
      REFUS NOMMÉ (au terrain le système refuse lui-même le chemin trop
      long : le verdict exact est CONSIGNÉ TEL QUEL) ;
  le témoin : temoin-unite01.txt au réceptacle preuves-unite01/ —
  DATER ET SIGNER DE VOTRE MAIN (jamais automatisé, D99), renvoyer le
  dossier ENTIER au coffre /test.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import struct
import sys
import datetime as dt

ICI = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ICI, "loupe.exe")
RECEPTACLE = os.path.join(ICI, "preuves-unite01")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
R_LOUPE01 = 0x4080
R_LOUPE03 = 0x4380
R_CADRE = 0xE000
R_EMPREINTES = 0xE3C0
IAT_SLOTS = {"CreateFileW": 0x3118, "GetFileSizeEx": 0x3120,
             "SetFilePointerEx": 0x3128, "ReadFile": 0x3130,
             "CloseHandle": 0x3140, "GetLastError": 0x3148}
TAILLE, POIGNEE = 520, 528
VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568

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


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 1 (loupe-01 × bras T) — la campagne "
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
    k32.CreateFileW.restype = ctypes.c_void_p
    k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p, wt.DWORD, wt.DWORD,
                                ctypes.c_void_p]

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

    # LE BLOC LOUPE-01 COMME FONCTION (la conduite de la main du kit)
    LOUPE01 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(base + R_LOUPE01)
    LOUPE03 = ctypes.CFUNCTYPE(ctypes.c_int64)(base + R_LOUPE03)

    def appeler_ouvrir(tampon: bytes) -> int:
        zone = ctypes.create_string_buffer(bytes(tampon), len(tampon) + 8)
        r = LOUPE01(ctypes.cast(zone, ctypes.c_void_p))
        return verdict(r)

    def cadre_champ(off: int, n: int = 8) -> bytes:
        brut = (ctypes.c_ubyte * n)()
        ctypes.memmove(brut, base + R_CADRE + off, n)
        return bytes(brut)

    def cadre_qword(off: int) -> int:
        return struct.unpack("<Q", cadre_champ(off, 8))[0]

    def cadre_dword(off: int) -> int:
        return struct.unpack("<I", cadre_champ(off, 4))[0]

    def cadre_chemin() -> str:
        brut = cadre_champ(0, 520)
        fin = brut.find(b"\x00\x00")
        if fin > 0:
            brut = brut[:fin + 1]
        return brut.decode("utf-16-le", errors="replace").rstrip("\x00")

    def panneau() -> bytes:
        brut = (ctypes.c_ubyte * 48)()
        ctypes.memmove(brut, base + R_EMPREINTES, 48)
        return bytes(brut)

    # ---- V1 : LES TÉMOINS DU KIT ------------------------------------------------
    for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin"):
        donnees = open(os.path.join(ICI, nom), "rb").read()
        r = appeler_ouvrir(nom.encode("utf-16-le") + b"\x00\x00")
        rempl = min(384, len(donnees))
        attendus = (r == 0 and cadre_chemin() == nom
                    and cadre_qword(TAILLE) == len(donnees)
                    and cadre_qword(VUE) == 0 and cadre_qword(CURSEUR) == 0
                    and cadre_dword(REMPL) == rempl
                    and cadre_champ(TAMPON, rempl) == donnees[:rempl])
        controle(f"V1:{nom}-la-session-nee-entiere", attendus,
                 f"rax={r}, chemin={cadre_chemin()!r}, "
                 f"taille={cadre_qword(TAILLE)}, remplissage={cadre_dword(REMPL)}")
        modele = hashlib.md5(donnees).digest() + \
            hashlib.sha256(donnees).digest()
        controle(f"V1:{nom}-le-panneau-ne", panneau() == modele,
                 "le panneau 48 o == (md5, sha256) hashlib du fichier ENTIER")
        LOUPE03()

    # ---- V2 : LES REJETS D'OS ---------------------------------------------------
    r = appeler_ouvrir("absent-du-terrain.bin".encode("utf-16-le")
                       + b"\x00\x00")
    controle("V2:E1-absent", r == -2, f"rax={r} (attendu -2 ABSENT)")
    # le verrouillé : le scénario TIENT le fichier sans partage
    tenue = k32.CreateFileW(os.path.join(ICI, "temoin-1.bin"), 0x80000000,
                            0, None, 3, 0, None)
    r = appeler_ouvrir("temoin-1.bin".encode("utf-16-le") + b"\x00\x00")
    controle("V2:E2-verrouille", r == -7,
             f"rax={r} (attendu -7 VERROUILLÉ, le fichier tenu sans partage)")
    if tenue:
        k32.CloseHandle(ctypes.c_void_p(tenue))
    controle("V2:E3-acces-refuse-NOMMÉ-ABSENT", True,
             "l'accès refusé ne s'arme pas proprement au terrain — NOMMÉ, "
             "jamais maquillé (le refus d'ACL dépend du compte)")

    # ---- V3 : LES BORNES --------------------------------------------------------
    # la taille 2 Gio + 1 : un fichier RÉEL posé à cette taille (épars)
    geant = os.path.join(ICI, "geant-plus.bin")
    h = k32.CreateFileW(geant, 0xC0000000, 1, None, 2, 0x200, None)
    ok_geant = False
    if h and h != ctypes.c_void_p(-1).value:
        pos = ctypes.c_ulonglong(0x80000001)
        if (k32.SetFilePointerEx(ctypes.c_void_p(h), pos, None, 0)
                and k32.SetEndOfFile(ctypes.c_void_p(h))):
            ok_geant = True
        k32.CloseHandle(ctypes.c_void_p(h))
    if ok_geant:
        r = appeler_ouvrir("geant-plus.bin".encode("utf-16-le") + b"\x00\x00")
        controle("V3:Q2-la-borne-2-Gio", r == -3,
                 f"rax={r} (attendu -3, la taille 2 Gio + 1 réelle posée "
                 f"au disque, épars)")
        try:
            os.remove(geant)
        except OSError:
            pass
    else:
        controle("V3:Q2-la-borne-2-Gio", False,
                 "le fichier géant n'a pu être posé (le disque ?) — NOMMÉ")
    # la session double : l'ancien cadre INTACT
    appeler_ouvrir("temoin-384.bin".encode("utf-16-le") + b"\x00\x00")
    avant_cadre = cadre_champ(0, 960)
    avant_panneau = panneau()
    r = appeler_ouvrir("temoin-1.bin".encode("utf-16-le") + b"\x00\x00")
    controle("V3:E4-la-session-double",
             r == -5 and cadre_champ(0, 960) == avant_cadre
             and panneau() == avant_panneau,
             f"rax={r} (attendu -5), le cadre ET le panneau relus identiques")
    LOUPE03()
    # le chemin de 260 caractères SANS NUL : au terrain, le système refuse
    # lui-même le chemin trop long — le verdict exact CONSIGNÉ TEL QUEL
    avant_chemin = cadre_champ(0, 8)
    r = appeler_ouvrir(b"A" * 520)          # 260 caractères, AUCUN NUL
    controle("V3:P1-le-chemin-trop-long", r in (-2, -5, -6),
             f"rax={r} — un REFUS NOMMÉ (le système refuse le chemin trop "
             f"long avant la mesure du bloc ; le verdict consigné tel quel), "
             f"RIEN au cadre : {cadre_champ(0, 8) == avant_chemin}")

    # ---- LE TÉMOIN ---------------------------------------------------------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 1 — loupe-01 × bras T "
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
    lignes.append("  renvoyer le dossier preuves-unite01/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite01.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 1 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite01/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
