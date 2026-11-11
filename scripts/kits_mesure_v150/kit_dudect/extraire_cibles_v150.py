#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_cibles_v150.py — L'EXTRACTEUR DES CIBLES DU KIT DUDECT v0.15.0.

La commande (ic09ydeli, point 2) : « kit dudect temps réel pour les
familles crypto sur la machine Windows du développeur (RDTSC/QPC, affinité
cœur, turbo désactivé si possible, protocole consigné) ». Le mesureur C
(dudect_v150.c) exécute les blocs des PIÈCES SCELLÉES — jamais une
ré-assemblée.

LA LEÇON DE L'ÉPREUVE (vécue au labo ce jour, le test_appel.c initial) :
les blocs ne sont PAS autonomes — tls13-02 lit sa table K par adressage
RIP-relatif vers .rdata (RVA 0x2F00) : un bloc mmapé seul FAUTE. La
découpe honnête n'est donc PAS le bloc isolé mais L'IMAGE MÉMOIRE
ÉTENDUE : la pièce réorganisée en mémoire (chaque section posée à son
RVA, la taille SizeOfImage) — le mesureur la mmap et appelle le bloc à
base + RVA, exactement comme le chargeur Windows (l'image est
RIP-relative par design — AUCUN appel indirect, charte § 7).

LA CHAÎNE DE CONFIANCE : l'extracteur recoupe d'abord le sha256 de la
PIÈCE contre l'empreinte scellée (proxy.exe 1.0.0 = 446279f3…, D-密封),
construit l'image étendue, en consigne le sha256 AU manifeste — le
mesureur re-recoupe l'image AVANT toute exécution (aucune confiance,
même pas à l'extracteur).

LES QUATRE CIBLES (la sélection — les blocs ISOLABLES, contrats de
couche I sans contexte d'application) :
  tls13-02  la compression SHA-256 (rcx=etat u32[8], rdx=bloc u8[64])
  tls13-13  l'échelle X25519 (rcx=sortie, rdx=scalaire, r8=u)
  tls13-16  le bloc AES-128 (rcx=cles[176], rdx=entree[16], r8=sortie)
  tls13-17  le GHASH (rcx=Z, rdx=X, r8=Y)

LA LIMITE CONSIGNÉE : loupe-06 (md5) vit SOUS SESSION (contrat P1) :
NON isolable sans l'application entière — l'itération future du kit (la
mesure pipeline de loupe.exe) ; AUCUN chiffre n'existe.

Sortie : kit_dudect/cibles/proxy-image.bin + manifeste.json — ÉPROUVÉ
AU LABO : le test d'appel FIPS « abc » (test_appel.c) rend le condensé
exact de la pièce scellée.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
import pefile  # noqa: E402

PIECE = {
    "chemin": REPO / "tls13" / "proxy.exe",
    "sha256_attendu": ("446279f3ab356900870cc3b3e1700654a4216ec0b264172"
                       "340e453db3b00d93d"),
    "nom": "proxy.exe 1.0.0 (M3, la pièce scellée)",
}

# la sélection : (nom, RVA du bloc, taille du slot, le contrat)
CIBLES = [
    ("tls13-02", 0xC080, 0x1C0,
     "compression SHA-256 : rcx=etat u32[8], rdx=bloc u8[64]"),
    ("tls13-13", 0xD100, 0xB80,
     "echelle X25519 : rcx=sortie u8[32], rdx=scalaire u8[32], r8=u u8[32]"),
    ("tls13-16", 0xDF00, 0xC0,
     "bloc AES-128 : rcx=cles u8[176], rdx=entree u8[16], r8=sortie u8[16]"),
    ("tls13-17", 0xDFC0, 0xC0,
     "GHASH GF(2^128) : rcx=Z u8[16], rdx=X u8[16], r8=Y u8[16]"),
]


def main():
    sortie = pathlib.Path(__file__).resolve().parent / "cibles"
    sortie.mkdir(exist_ok=True)

    donnees = PIECE["chemin"].read_bytes()
    empreinte = hashlib.sha256(donnees).hexdigest()
    if empreinte != PIECE["sha256_attendu"]:
        print(f"[REFUS] {PIECE['chemin'].name} : sha256 {empreinte[:12]}… "
              f"≠ scellé {PIECE['sha256_attendu'][:12]}… — la pièce a bougé, "
              f"RIEN n'est extrait")
        sys.exit(2)
    print(f"[pièce] {PIECE['chemin'].name} : scellé INTACT {empreinte[:12]}…")

    pe = pefile.PE(str(PIECE["chemin"]), fast_load=True)
    taille_image = pe.OPTIONAL_HEADER.SizeOfImage
    base_image = pe.OPTIONAL_HEADER.ImageBase
    # l'image mémoire étendue : les octets posés aux RVA (les trous à zéro)
    image = bytearray(taille_image)
    image[:len(donnees)] = donnees[:min(len(donnees), taille_image)]
    for sec in pe.sections:
        fin = min(sec.PointerToRawData + sec.SizeOfRawData, len(donnees))
        image[sec.VirtualAddress:sec.VirtualAddress + (fin - sec.PointerToRawData)] = \
            donnees[sec.PointerToRawData:fin]
    image_bin = sortie / "proxy-image.bin"
    image_bin.write_bytes(bytes(image))
    sha_image = hashlib.sha256(bytes(image)).hexdigest()
    print(f"[image] {taille_image} octets étendus "
          f"(ImageBase {base_image:#x}), sha256 {sha_image[:12]}…")

    manifeste = {
        "piece": {"fichier": PIECE["chemin"].name,
                  "sha256": empreinte, "nom": PIECE["nom"]},
        "image": {"fichier": "proxy-image.bin", "taille": taille_image,
                  "image_base": base_image, "sha256": sha_image},
        "cibles": [
            {"nom": nom, "rva": rva, "taille_slot": taille,
             "sha256_plage": hashlib.sha256(bytes(image[rva:rva + taille])).hexdigest(),
             "contrat": contrat}
            for nom, rva, taille, contrat in CIBLES
        ],
        "limite_consignee": (
            "loupe-06 (md5) vit sous session (contrat P1) : NON isolable "
            "sans l'application entière — la mesure pipeline de loupe.exe "
            "appartient à une itération future du kit ; AUCUN chiffre "
            "n'existe."),
    }
    (sortie / "manifeste.json").write_text(
        json.dumps(manifeste, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    # le manifeste SIMPLE pour le mesureur C (le format trivial, aucun
    # parse JSON en C — la même information, la source unique est le .json)
    lignes = [f"image {sha_image}", f"taille {taille_image}"]
    for c in manifeste["cibles"]:
        lignes.append(f"cible {c['nom']} {c['rva']} {c['taille_slot']} "
                      f"{c['sha256_plage']}")
    (sortie / "manifeste-c.txt").write_text("\n".join(lignes) + "\n",
                                            encoding="utf-8")
    for c in manifeste["cibles"]:
        print(f"[cible] {c['nom']} : RVA {c['rva']:#x}, slot "
              f"{c['taille_slot']:#x} o, sha256 plage "
              f"{c['sha256_plage'][:12]}…")
    print(f"[sortie] {sortie}/ : proxy-image.bin + manifeste.json "
          f"({len(CIBLES)} cibles)")


if __name__ == "__main__":
    main()
