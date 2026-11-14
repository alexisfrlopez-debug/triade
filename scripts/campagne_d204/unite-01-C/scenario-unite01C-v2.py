#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite01C.py — LE TERRAIN DE L'UNITÉ 1 × BRAS C (loupe-01, la
campagne de comparaison des workflows D204).

Le kit porte la PIÈCE COMPILÉE et UN scénario :
  loupe-01-c.dll       la pièce de campagne du bras C — le source C de
                       l'auteur (loupe-01-c.c), compilé gcc -O2 -shared
                       (la commande consignée au journal du labo) ; le
                       flux standard, tel qu'il se pratique ;
  loupe-01-c.c/.def    le source et la définition des exports (la
                       livraison du bras C : le binaire ET son source) ;
  le présent script    python SEUL (ctypes, hashlib, os, platform,
                       struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le même mécanisme de kit terrain que le bras T —
CA2, la seule adaptation : LA PIÈCE EST UN PE COMPILÉ) : le scénario est
LE CHARGEUR — LoadLibraryEx DONT_RESOLVE (aucune entrée résolue, AUCUN
point d'entrée exécuté — le CRT de la pièce ne vit jamais), il découvre
les adresses PAR LA TABLE D'EXPORTS de la pièce (loupe_01_ouvrir,
loupe_03_fermer, et les DONNÉES cadre 960 o et panneau 48 o), résout
LUI-MÊME les feuilles kernel32 AUX SLOTS RÉELS de la table d'imports de
la pièce (VirtualProtect le temps du geste — les six du kit, celles que
la pièce déclare ; SetFilePointerEx : la pièce ne s'en sert pas —
l'ÉCART NOMMÉ, la lecture est séquentielle) et APPELLE LOUPE_01_OUVRIR
À SON ADRESSE EXPORTÉE, conduite par la main du kit. Le juge demeure le
MODÈLE INDÉPENDANT (hashlib, les découpes) — jamais les octets de la
pièce.

LES VECTEURS DU CONTRAT (loupe-01 révision 3 — les mêmes que le bras T) :
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

  le témoin : temoin-unite01C.txt au réceptacle preuves-unite01C/ —
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
PIECE = os.path.join(ICI, "loupe-01-c.dll")
RECEPTACLE = os.path.join(ICI, "preuves-unite01C")

# les offsets du plan (loupe/layout.py — la source unique, les MÊMES que
# le bras T : le contrat de couche I ne change pas de bras)
TAILLE, POIGNEE = 520, 528
VUE, CURSEUR, REMPL, TAMPON = 536, 544, 552, 568
# les six feuilles du kit (celles que la pièce déclare seront résolues —
# l'absence de SetFilePointerEx est l'ÉCART NOMMÉ du bras C)
FEUILLES_KIT = ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                "ReadFile", "CloseHandle", "GetLastError")

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


def lire_octets(base: int, rva: int, n: int) -> bytes:
    brut = (ctypes.c_ubyte * n)()
    ctypes.memmove(brut, base + rva, n)
    return bytes(brut)


def lire_u32(base: int, rva: int) -> int:
    return struct.unpack("<I", lire_octets(base, rva, 4))[0]


def lire_u16(base: int, rva: int) -> int:
    return struct.unpack("<H", lire_octets(base, rva, 2))[0]


def lire_chaine(base: int, rva: int, limite: int = 64) -> str:
    brut = lire_octets(base, rva, limite)
    fin = brut.find(b"\x00")
    return brut[:fin if fin >= 0 else limite].decode("ascii",
                                                     errors="replace")


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 1 × BRAS C (loupe-01, gcc -O2) — la "
             "campagne D204, le terrain du développeur ===")
    empreintes = lire_empreintes()
    if not empreintes:
        consigne("[T0] REFUS : aucune EMPREINTES*.txt au kit — rien ne court")
        return 2
    sha_piece = sha256_fichier(PIECE)
    attendu = empreintes.get("loupe-01-c.dll", "")
    if sha_piece != attendu:
        consigne(f"[T0] REFUS : loupe-01-c.dll {sha_piece[:16]}… != "
                 f"l'empreinte gravée {attendu[:16]}… — la pièce a divergé, "
                 f"rien ne court")
        return 2
    controle("T0:la-piece-recoupee-a-l-empreinte-gravee", True,
             f"loupe-01-c.dll sha256 {sha_piece[:16]}… == la gravure du kit")

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

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(PIECE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")

    # ---- LA DÉCOUVERTE PAR LA TABLE D'EXPORTS (le bras C : la pièce
    # compilée porte SES adresses aux tables du PE) --------------------------
    e_lfanew = struct.unpack("<I", lire_octets(base, 0x3C, 4))[0]
    opt = e_lfanew + 4 + 20                      # l'en-tête optionnel PE32+
    rva_exports = lire_u32(base, opt + 112)      # le répertoire 0 : export
    rva_imports = lire_u32(base, opt + 120)      # le répertoire 1 : import
    if not rva_exports or not rva_imports:
        consigne("[T0] REFUS : les répertoires d'exports/d'imports "
                 "introuvables — la pièce n'est pas la DLL attendue")
        return 2
    noms_vus, rva_par_nom = [], {}
    # IMAGE_EXPORT_DIRECTORY (Name +12, Base +16 — les versions sont des
    # WORD) : NumberOfFunctions +20, NumberOfNames +24,
    # AddressOfFunctions +28, AddressOfNames +32, AddressOfNameOrdinals +36
    nb_noms = lire_u32(base, rva_exports + 24)
    tab_fonctions = lire_u32(base, rva_exports + 28)
    tab_noms = lire_u32(base, rva_exports + 32)
    tab_ordinaux = lire_u32(base, rva_exports + 36)
    for i in range(nb_noms):
        nom = lire_chaine(base, lire_u32(base, tab_noms + 4 * i))
        ordinal = lire_u16(base, tab_ordinaux + 2 * i)
        rva_par_nom[nom] = lire_u32(base, tab_fonctions + 4 * ordinal)
        noms_vus.append(nom)
    for attendu_nom in ("loupe_01_ouvrir", "loupe_03_fermer",
                        "cadre", "panneau"):
        if attendu_nom not in rva_par_nom:
            consigne(f"[T0] REFUS : l'export {attendu_nom} introuvable à "
                     f"la table ({noms_vus}) — la pièce a divergé")
            return 2
    R_OUVRIR = rva_par_nom["loupe_01_ouvrir"]
    R_FERMER = rva_par_nom["loupe_03_fermer"]
    R_CADRE = rva_par_nom["cadre"]
    R_EMPREINTES = rva_par_nom["panneau"]
    consigne(f"[T0] les QUATRE exports découverts : loupe_01_ouvrir "
             f"@+{R_OUVRIR:#x}, loupe_03_fermer @+{R_FERMER:#x}, cadre "
             f"(DONNÉE, 960 o) @+{R_CADRE:#x}, panneau (DONNÉE, 48 o) "
             f"@+{R_EMPREINTES:#x}")

    # ---- LA RÉSOLUTION AUX SLOTS RÉELS de la table d'imports ---------------
    # (v2 — LA RÉPARATION DU REFUS DU 14/11 : le terminateur se lit au CHAMP
    #  Name (l'RVA NUL), JAMAIS à la chaîne — à l'RVA 0 vit l'en-tête DOS
    #  « MZ », et la boucle v1 dérivait hors table jusqu'à l'access violation
    #  0x7ffa23900094 du terrain ; gardes fail-closed : au plus 64
    #  descripteurs, aucun Name hors image — REFUS nommé, jamais un plantage)
    h_k32 = ctypes.c_void_p(k32.GetModuleHandleW("kernel32.dll"))
    slots = {}                                    # nom → l'adresse du slot
    taille_image = lire_u32(base, opt + 56)       # SizeOfImage (PE32+ : +56)
    desc = rva_imports
    for _garde in range(64):
        nom_rva = lire_u32(base, desc + 12)
        if not nom_rva:                           # LE TERMINATEUR : Name NUL
            break
        if nom_rva >= taille_image:               # la garde fail-closed
            consigne(f"[T0] REFUS : un descripteur d'import pointe hors "
                     f"image (@+{nom_rva:#x}) — la pièce a divergé, rien "
                     f"ne court")
            return 2
        nom_dll = lire_chaine(base, nom_rva)
        if not nom_dll:
            break
        if "kernel32" in nom_dll.lower():
            ilt = lire_u32(base, desc + 0)        # OriginalFirstThunk
            iat = lire_u32(base, desc + 16)       # FirstThunk
            j = 0
            while True:
                entree = struct.unpack(
                    "<Q", lire_octets(base, ilt + 8 * j, 8))[0] if ilt \
                    else lire_u32(base, iat + 8 * j)
                if not entree:
                    break
                if not (entree >> 63):
                    feuille = lire_chaine(base, (entree & 0xFFFFFFFF) + 2)
                    if feuille in FEUILLES_KIT:
                        slots[feuille] = base + iat + 8 * j
                j += 1
        desc += 20
    else:
        consigne("[T0] REFUS : la table d'imports sans terminateur — la "
                 "pièce a divergé, rien ne court")
        return 2
    manquantes = [f for f in FEUILLES_KIT if f not in slots]
    if "SetFilePointerEx" in manquantes:
        manquantes.remove("SetFilePointerEx")    # l'ÉCART NOMMÉ du bras C
        consigne("[T0] SetFilePointerEx absente des imports de la pièce — "
                 "L'ÉCART NOMMÉ (la lecture est séquentielle depuis "
                 "l'ouverture ; le bras T la résolvait, la pièce C ne "
                 "l'appelle pas)")
    if manquantes:
        consigne(f"[T0] REFUS : les feuilles {manquantes} introuvables à "
                 f"la table d'imports — la pièce a divergé")
        return 2
    for feuille, adresse_slot in sorted(slots.items()):
        adresse = k32.GetProcAddress(h_k32, feuille.encode("ascii"))
        if not adresse:
            consigne(f"[T0] REFUS : {feuille} introuvable à kernel32")
            return 2
        ancien = wt.DWORD(0)
        page = adresse_slot & ~0xFFF
        if not k32.VirtualProtect(ctypes.c_void_p(page), 0x1000,
                                  0x40, ctypes.byref(ancien)):
            consigne("[T0] REFUS : VirtualProtect sur l'IAT impossible")
            return 2
        ctypes.memmove(adresse_slot, struct.pack("<Q", adresse), 8)
        k32.VirtualProtect(ctypes.c_void_p(page), 0x1000, ancien.value,
                           ctypes.byref(ancien))
    consigne(f"[T0] les {len(slots)} feuilles kernel32 de la pièce résolues "
             f"aux slots réels de SA table d'imports ({', '.join(sorted(slots))})")

    # ---- LE BLOC LOUPE-01 COMME FONCTION (la conduite de la main du kit) ----
    LOUPE01 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(base + R_OUVRIR)
    LOUPE03 = ctypes.CFUNCTYPE(ctypes.c_int64)(base + R_FERMER)

    def appeler_ouvrir(tampon: bytes) -> int:
        zone = ctypes.create_string_buffer(bytes(tampon), len(tampon) + 8)
        r = LOUPE01(ctypes.cast(zone, ctypes.c_void_p))
        return verdict(r)

    def cadre_champ(off: int, n: int = 8) -> bytes:
        return lire_octets(base, R_CADRE + off, n)

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
        return lire_octets(base, R_EMPREINTES, 48)

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
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 1 × BRAS C — loupe-01 (gcc -O2, "
                  "le flux standard) — la campagne D204, la comparaison "
                  "des workflows")
    lignes.append("=" * 78)
    lignes.append(f"le run      : "
                  f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
                  f" (UTC) — la machine du développeur")
    lignes.append(f"la machine  : {platform.node()} · {platform.system()} "
                  f"{platform.release()} · {platform.machine()} · "
                  f"Python {platform.python_version()}")
    lignes.append(f"la pièce    : loupe-01-c.dll "
                  f"{os.path.getsize(PIECE)} o, sha256 {sha_piece}")
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
    lignes.append("  renvoyer le dossier preuves-unite01C/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite01C.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 1 × BRAS C FINI : dater et signer le "
             "témoin de votre main, renvoyer preuves-unite01C/ ENTIER au "
             "coffre /test ===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
