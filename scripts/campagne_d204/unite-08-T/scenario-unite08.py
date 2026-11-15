#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-unite08.py — LE TERRAIN DE L'UNITÉ 4 (loupe-08 ligne × bras T,
la campagne de comparaison des workflows D204).

Le kit porte UNE pièce et UN scénario :
  loupe.exe          la pièce de campagne — le build du plan où le slot
                     loupe-08 (RVA 0x49C0, 320 o) porte LA NOTATION DE
                     CAMPAGNE écrite à la main par l'agent (296 o, 85
                     instructions — le contrat loupe-08:R1 : composer UNE
                     ligne hexadécimale de 77 o au tampon fixe — les 8
                     chiffres du décalage, les seize groupes « HH » à
                     l'espace médian doublé, le miroir ASCII, le NUL ;
                     AUCUN débordement par construction, AUCUNE entrée
                     IAT — la feuille pure) ; les dix-sept autres blocs
                     demeurent les SCELLÉS du projet ;
  le présent script  python SEUL (ctypes, hashlib, os, platform, random,
                     struct, sys — AUCUN paquet à installer).

LE GESTE DU SCÉNARIO (le modèle de la campagne Loupe, inchangé — la
feuille pure le simplifie à l'extrême) : le scénario est LE CHARGEUR —
LoadLibraryEx DONT_RESOLVE (aucune entrée résolue, AUCUN point d'entrée
exécuté) ; LA FEUILLE PURE N'APPELLE PERSONNE : aucune feuille kernel32
à résoudre, le scénario ne touche pas à l'IAT — il APPELLE LOUPE-08 À
SON ADRESSE AU PLAN (base + 0x49C0), conduit par la main du kit. Le
juge est le MODÈLE INDÉPENDANT (la composition Python du format) —
jamais les octets du bloc.

LES VECTEURS DU CONTRAT (loupe-08 révision 1) :
  V1  le doré : LA PREMIÈRE LIGNE DE PROXY.EXE SCELLÉ (la pièce de
      l'ère rendue à l'œil — sa première ligne : « 4D 5A 00 00… », le
      projet écrit ses en-têtes à la main, la citation canonique
      « MZ\x90\x00\x03 » du contrat est l'illustration, l'octet du
      scellé est la vérité) : la ligne exacte, les 77 o comparés au
      modèle ; LA LIGNE FINALE INCOMPLÈTE du témoin de 3 × 64 Kio + 1
      (UN octet valide : quinze groupes d'espaces, la colonne droite) ;
  V2  le différentiel : 10 000 lignes aléatoires (décalages multiples
      de 16 ≤ 0x7FFFFFFF, longueurs 1..16, octets 0x00..0xFF — la
      graine fixe 20261115, les mêmes tirages au labo et au terrain) :
      la sortie == la composition Python du même format, l'égalité
      OCTET PAR OCTET ; la sortie empoisonnée à 96 o : EXACTEMENT 77
      écrits — le poison au-delà demeure (I2 : jamais un de plus) ;
  V3  les rejets : longueur 0, longueur 17, source nulle, sortie nulle
      → les QUATRE verdicts -5, RIEN écrit (la sortie POISON INTACTE) ;
  V4  la falsification demandée : le doré COPIÉ AU RÉCEPTACLE avec un
      octet muté — la même gamme rend une ligne QUI DIVERGE du modèle
      de l'original ET == le modèle du mutant : la pièce a lu SES
      octets, la différentielle attrape le faux (le fixture
      falsifie-16.bin vit au réceptacle preuves-unite08/, renvoyé
      ENTIER avec le témoin).

  le témoin : temoin-unite08.txt au réceptacle preuves-unite08/ —
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
RECEPTACLE = os.path.join(ICI, "preuves-unite08")

# LES CONSTANTES DU PLAN (loupe/layout.py — la source unique)
R_LOUPE08 = 0x49C0
GRAINE = 20261115
LIGNE = 77
POISON = b"\xCC"

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


def modele_ligne(decalage: int, octets: bytes) -> bytes:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat, jamais les octets
    du bloc : la ligne de 77 o exacts."""
    s = f"{decalage:08X}  "
    g = [f"{b:02X}" if i < len(octets) else "  "
         for i, b in enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(g[:8]) + "  " + " ".join(g[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"          # 77 o exacts


def main() -> int:
    consigne("=== LE RUN DE L'UNITÉ 4 (loupe-08 ligne × bras T) — la "
             "campagne D204, le terrain du développeur ===")
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

    DONT_RESOLVE = 0x00000001
    base = k32.LoadLibraryExW(EXE, None, DONT_RESOLVE)
    if not base:
        consigne(f"[T0] REFUS : LoadLibraryEx a rendu 0 (GetLastError "
                 f"{ctypes.get_last_error()})")
        return 2
    consigne(f"[T0] l'image cartographiée DONT_RESOLVE @ {base:#x}")
    consigne("[T0] la feuille pure : AUCUNE feuille kernel32 à résoudre — "
             "le scénario ne touche pas à l'IAT, la pièce n'appelle personne")

    # LE BLOC COMME FONCTION (la conduite de la main du kit)
    LOUPE08 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64)(base + R_LOUPE08)

    source_buf = ctypes.create_string_buffer(16)
    sortie_buf = ctypes.create_string_buffer(96)

    def composer(source: bytes, longueur: int, decalage: int) \
            -> tuple[int, bytes]:
        """Le geste de la campagne : la sortie POISONNÉE à 96 o avant
        l'appel (les refus ne publient RIEN, jamais un de plus)."""
        ctypes.memmove(source_buf, source, 16)
        ctypes.memmove(sortie_buf, POISON * 96, 96)
        r = LOUPE08(ctypes.cast(source_buf, ctypes.c_void_p), longueur,
                    ctypes.cast(sortie_buf, ctypes.c_void_p), decalage)
        brut = (ctypes.c_ubyte * 96)()
        ctypes.memmove(brut, sortie_buf, 96)
        return verdict(r), bytes(brut)

    # ---- V1 : LE DORÉ — la première ligne du scellé + la ligne finale ----
    premiere = open(os.path.join(ICI, "proxy.exe"), "rb").read(16)
    r, ligne = composer(premiere + b"\x00" * (16 - len(premiere)), 16, 0)
    attendu_l = modele_ligne(0, premiere)
    controle("V1:le-dore-proxy-premiere-ligne",
             r == 0 and ligne[:LIGNE] == attendu_l
             and ligne[LIGNE:] == POISON * 19,
             f"les 77 o == le modèle (« {attendu_l[:32].decode('latin-1')}… »"
             " — la pièce de l'ère rendue à l'œil)")

    temoin3f = open(os.path.join(ICI, "temoin-3f.bin"), "rb").read()
    if len(temoin3f) != 3 * 65536 + 1:
        consigne(f"[V1] REFUS : temoin-3f.bin {len(temoin3f)} o != 196 609 o "
                 "— le fixture du kit a divergé")
        return 2
    finale = temoin3f[-1:]
    r, ligne = composer(finale + b"\x00" * 15, 1, 3 * 65536)
    attendu_l = modele_ligne(3 * 65536, finale)
    controle("V1:le-temoin-3f-ligne-finale-incomplete",
             r == 0 and ligne[:LIGNE] == attendu_l
             and ligne[LIGNE:] == POISON * 19,
             "UN octet valide : quinze groupes d'espaces, la colonne ASCII "
             "droite — Q3")

    # ---- V2 : LE DIFFÉRENTIEL — 10 000 lignes aléatoires ------------------
    rng = random.Random(GRAINE)
    ecarts, ecarts_poison = 0, 0
    for _ in range(10_000):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = rng.randbytes(16)
        r, ligne = composer(source, longueur, decalage)
        if r != 0 or ligne[:LIGNE] != modele_ligne(decalage,
                                                   source[:longueur]):
            ecarts += 1
        if ligne[LIGNE:] != POISON * 19:
            ecarts_poison += 1
    controle("V2:le-differentiel-10-000-lignes", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (la graine {GRAINE}, "
             "les mêmes tirages au labo)")
    controle("V2:exactement-77-o", ecarts_poison == 0,
             "le poison au-delà de 77 demeure aux 10 000 gestes (I2 : "
             "jamais un de plus)")

    # ---- V3 : LES REJETS — les quatre -5, RIEN écrit -----------------------
    source16 = bytes(range(0x10, 0x20))
    ctypes.memmove(source_buf, source16, 16)
    for nom, src, lon, srt in (
            ("E1:la-longueur-nulle", source_buf, 0, sortie_buf),
            ("E2:la-longueur-dix-sept", source_buf, 17, sortie_buf),
            ("E3:la-source-nulle", None, 5, sortie_buf),
            ("E3:la-sortie-nulle", source_buf, 5, None)):
        ctypes.memmove(sortie_buf, POISON * 96, 96)
        r = verdict(LOUPE08(ctypes.cast(src, ctypes.c_void_p)
                            if src is not None else None,
                            lon,
                            ctypes.cast(srt, ctypes.c_void_p)
                            if srt is not None else None,
                            0))
        brut = (ctypes.c_ubyte * 96)()
        ctypes.memmove(brut, sortie_buf, 96)
        intact = bytes(brut) == POISON * 96
        controle(f"V3:{nom}", r == -5 and intact,
                 f"verdict {r}, la sortie POISON INTACTE — rien écrit")

    # ---- V4 : LA FALSIFICATION DEMANDÉE — l'octet muté ---------------------
    os.makedirs(RECEPTACLE, exist_ok=True)
    mutant = bytearray(premiere)
    mutant[3] ^= 0x6F                    # l'octet 3 muté — le faux né
    mutant = bytes(mutant)
    chemin_faux = os.path.join(RECEPTACLE, "falsifie-16.bin")
    with open(chemin_faux, "wb") as f:
        f.write(mutant)
    r, ligne = composer(mutant, 16, 0)
    diverge = ligne[:LIGNE] != modele_ligne(0, premiere)
    egale_mutant = ligne[:LIGNE] == modele_ligne(0, mutant)
    controle("V4:l-octet-mute-la-ligne-diverge",
             r == 0 and diverge and egale_mutant,
             "l'octet 3 muté : la ligne DIVERGE du modèle de l'original ET "
             "== le modèle du mutant — la pièce a lu SES octets, la "
             "différentielle attrape le faux (le fixture falsifie-16.bin "
             "vit au réceptacle)")

    # ---- LE TÉMOIN ----------------------------------------------------------
    lignes = []
    lignes.append("TÉMOIN DU RUN DE L'UNITÉ 4 — loupe-08 ligne × bras T "
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
    lignes.append("  renvoyer le dossier preuves-unite08/ ENTIER au coffre /test.")
    lignes.append("")
    lignes.append("Daté le : ____________________")
    lignes.append("Signé    : ____________________")
    chemin_temoin = os.path.join(RECEPTACLE, "temoin-unite08.txt")
    with open(chemin_temoin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    consigne(f"[témoin] {chemin_temoin} — {len(REUSSITES)} VERT, "
             f"{len(ECARTS)} ROUGE")
    consigne("=== LE RUN DE L'UNITÉ 4 FINI : dater et signer le témoin de "
             "votre main, renvoyer preuves-unite08/ ENTIER au coffre /test "
             "===")
    return 0 if not ECARTS else 1


if __name__ == "__main__":
    sys.exit(main())
