#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shani/layout.py — LE PLAN D'ADRESSAGE DE LA VARIANTE SHA-NI (le paquet 6/6
de la vague 3, l'instruction lfh49a1xf — D205).

LA VARIANTE DE PROFIL sha256 : une famille de TROIS blocs qui porte LE MÊME
CONTRAT que la famille sha scellée M9 (tls13-01..04) avec la compression
exécutée par les instructions SHA-NI du processeur — sélectionnée au geste
par dispatch CPUID (shani-01 la sonde), le repli scalaire APPELANT LES
BLOCS SCELLÉS EXISTANTS à leurs adresses d'origine (R7 : 0xC000-0xC3C0,
octet-identiques dans loupe.exe — le plan loupe est LA source, importé par
chemin nominatif, jamais recopié).

LA ZONE : la marge .text2 0xD000-0xDFFF — INT3 VIERGE dans le scellé
loupe.exe (constaté sur pièces : 3 584 octets 0xCC), après la famille sha
scellée (0xC000-0xC3C0), avant .data (0xE000). La variante N'Y VIT PAS
encore : aucun scellement, aucune cérémonie — les blocs sont des COPIES DE
LABORATOIRE aux adresses du plan ; ils naîtront dans l'image au geste du
développeur (la prochaine cérémonie d'ère), JAMAIS avant.

LES CONSTANTES : le masque BE @0x2800 (16 o — la marge .rdata VIERGE
constatée : 16 octets nuls dans loupe.exe) ; la table K @0x2F00 — LA TABLE
DU SCELLÉ, citée par déplacement RIP, JAMAIS re-déclarée (I2 de la spec :
tls13/layout.py demeure la source unique des 64 constantes FIPS).

LA PRÉFIGURATION N'EST PAS UN DROIT (D161) : les RVA et tailles définitifs
sont ARRÊTÉS à la passe d'auteur sur les LONGUEURS RÉELLES mesurées —
l'outil refuse tout débordement (D8 : multiple de 64, padding ≥ 16).
"""

import importlib.util
import os as _os

_TR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "layout_loupe", _os.path.join(_TR, "loupe", "layout.py"))
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

# --- LES ADRESSES SCELLÉES (R7 — le plan loupe, source unique, importé) ----------

R_TLS01 = L.R_TLS01             # 0xC000 — l'initialisation scellée M9
R_TLS02 = L.R_TLS02             # 0xC080 — la compression scellée (LE REPLI)
R_TLS03 = L.R_TLS03             # 0xC240 — l'absorption scellée
R_TLS04 = L.R_TLS04             # 0xC300 — la finalisation scellée
R_K = L.R_K                     # 0x2F00 — K[64] u32 du scellé (16 o alignée)

# --- LA ZONE DE LA VARIANTE (la marge .text2 vierge 0xD000-0xDFFF) --------------

# L'ARRÊT SUR LES MESURES (D161 — la passe d'auteur du 12/11 : 42/856/159 o
# notés → les slots MINIMUMS au pas de 64, padding ≥ 16, tassés à la
# contiguïté — le miroir de l'arrêt loupe) :
SHANI01_VA = 0xD000             # la sonde CPUID (0x40 : 42 o + 22 padding)
SHANI02_VA = 0xD080             # la compression SHA-NI (0x380 : 856 o + 40)
SHANI03_VA = 0xD400             # l'absorption à dispatch (0xC0 : 159 o + 33)
FIN_ZONE = 0xD4C0               # la réserve contiguë restante : 0xD4C0-0xDFFF

# --- LES CONSTANTES PUBLIQUES DE LA FAMILLE --------------------------------------

R_MASQUE = 0x2800               # le masque BE pshufb (16 o — marge .rdata
                                # VIERGE constatée dans loupe.exe : 16 o nuls)
MASQUE_BE = bytes([3, 2, 1, 0, 7, 6, 5, 4,
                   11, 10, 9, 8, 15, 14, 13, 12])
                                # chaque dword renversé — le chargement BE des
                                # mots du message (FIPS 180-4 : l'entier
                                # gros-boutiste lu en mémoire petit-boutiste)

# LES DRAPEAUX CPUID DE LA SONDE (les SEuls lus — la liste fermée) :
CPUID_SHA_BIT = 29              # feuille 7, sous-feuille 0, EBX bit 29 (SHA)
CPUID_SSSE3_BIT = 9             # feuille 1, ECX bit 9 (SSSE3 — pshufb/palignr)

# les groupes K : 16 × 16 o alignés dans la table du scellé (0x2F00 % 16 == 0 —
# le movdqa du cur vise K_Gg = R_K + 16·g, la source unique jamais dupliquée)
K_GROUPES = [R_K + 16 * g for g in range(16)]

# --- LES SLOTS (l'ARRÊT DÉFINITIF vit à la passe d'auteur, D161) -----------------

SLOTS_SHANI = {
    "g210001": (SHANI01_VA, 0x40),
    "g210002": (SHANI02_VA, 0x380),
    "g210003": (SHANI03_VA, 0xC0),
}

NOMS_COURTS = {
    "shani-01-sonde": "sonde CPUID SHA-NI+SSSE3",
    "shani-02-comprimer": "compression SHA-256 SHA-NI d'un bloc de 64 o",
    "shani-03-absorber": "absorption tamponnée à dispatch SHA-NI/scalaire",
}

# --- LE DOSSIER R11 (la mesure AVANT l'optimisation — l'évidence) -----------------

HOTPATH_PREUVES = _os.path.join("scripts", "preuves_v150", "hotpath_shani")
HOTPATH_MESURE = ("tls13-02 = 98,11 % des instructions exécutées du hachage "
                  "d'un fichier volumineux dans le harnais loupe (64 Kio et "
                  "256 Kio, graine 20261112 — mesure_hotpath.txt, consignée "
                  "AVANT le premier octet de la variante)")
