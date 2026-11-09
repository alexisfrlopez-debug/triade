#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA RETOUCHE DE L'ENTRÉE 214 — [OFT-QWORD] nommé, la pièce répond.

Le défaut (constaté sur les octets du run 9) : les QUATRE tableaux
OriginalFirstThunk sont écrits à PAS DE QWORD (RVA + 4 octets de zéro)
au lieu du PAS DE DWORD du format PE. Le VRAI chargeur lit OFT[1] = 0
et CROIT chaque liste terminée : UNE résolution par DLL, 33 slots IAT
péri­més (leur valeur fichier : les RVA hint/nom), le second appel de
l'entrée (GetCommandLineW, slot 0x3108) saute à l'adresse absolue
0x2A53 — non mappée — 0xC0000005 EXÉCUTION, module « unknown » —
LE BEX64 nommé par le journal d'événements du run 9.

LA RETOUCHE : les QUATRE tableaux compactés EN PLACE au pas de dword
[10 · 18 · 6 · 3 feuilles + terminateurs NULL], le slack rendu zéro —
les pointeurs OFT des descripteurs (0x28A0/0x2900/0x29A0/0x29E0)
INCHANGÉS, la table hint/nom (0x2A10+) INCHANGÉE, l'IAT FT INCHANGÉE,
le .text/.text2/.data/les en-têtes OCTET-IDENTIQUES — et le qword
version @0x2E80 porté 0x00010007 → 0x00010008 (loupe 0.1.0-dev.8).

La carte : génération 16 (patch en place, hors chaîne build_loupe.py —
la dette de régénération se poursuit, l'Entrée 211).
"""
import hashlib
import struct
import sys

SRC = "/home/z/my-project/run9/loupe.exe"
DST = "/home/z/my-project/build-dev10/loupe.exe"

OFT_K32 = 0x28A0
OFT_U32 = 0x2900
OFT_GDI = 0x29A0
OFT_DEMO = 0x29E0
R_VERSION = 0x2E80

donnees = bytearray(open(SRC, "rb").read())
assert len(donnees) == 127488, f"taille inattendue {len(donnees)}"
sha_avant = hashlib.sha256(donnees).hexdigest()
print(f"la pièce dev.7 : {len(donnees)} o, sha256 {sha_avant[:16]}…")

def f_rdata(rva):
    return 0x1200 + (rva - 0x2000)   # .rdata VA 0x2000, PR 0x1200

# --- 1. lire les valeurs qword-stridées actuelles ---------------------------
def lit_oft_qword(rva):
    vals, i = [], 0
    while True:
        q, = struct.unpack_from("<Q", donnees, f_rdata(rva) + 8 * i)
        if q == 0:
            return vals
        assert q < 0x10000, f"valeur OFT inattendue {q:#x}"
        vals.append(q)
        i += 1

k32 = lit_oft_qword(OFT_K32)
u32 = lit_oft_qword(OFT_U32)
gdi = lit_oft_qword(OFT_GDI)
demo = lit_oft_qword(OFT_DEMO)
print(f"les OFT lus (pas de qword) : kernel32 {len(k32)} · user32 "
      f"{len(u32)} · gdi32 {len(gdi)} · démo {len(demo)}")
assert (len(k32), len(u32), len(gdi), len(demo)) == (10, 18, 6, 3), \
    "les comptes OFT ne sont pas ceux du plan"

# --- 2. compacter en place au pas de dword -----------------------------------
def compacte(rva, vals, fin_borne):
    fo = f_rdata(rva)
    for i, v in enumerate(vals):
        struct.pack_into("<I", donnees, fo + 4 * i, v)
    struct.pack_into("<I", donnees, fo + 4 * len(vals), 0)   # le terminateur
    debut_slack = fo + 4 * (len(vals) + 1)
    for p in range(debut_slack, f_rdata(fin_borne)):
        donnees[p] = 0
    return 4 * (len(vals) + 1)

n1 = compacte(OFT_K32, k32, OFT_U32)     # le slack rendu zéro jusqu'à 0x2900
n2 = compacte(OFT_U32, u32, OFT_GDI)
n3 = compacte(OFT_GDI, gdi, OFT_DEMO)
n4 = compacte(OFT_DEMO, demo, 0x2A00)
print(f"compactés : {n1} · {n2} · {n3} · {n4} octets (avec terminateurs)")

# --- 3. le qword version porté à dev.8 ---------------------------------------
ancien, = struct.unpack_from("<Q", donnees, f_rdata(R_VERSION))
assert ancien == 0x00010007, f"qword version inattendu {ancien:#x}"
struct.pack_into("<Q", donnees, f_rdata(R_VERSION), 0x00010008)

# --- 4. LA VÉRIFICATION COMPLÈTE ---------------------------------------------
# 4a. la marche du VRAI chargeur sur les OFT compactés (pas de DWORD, arrêt
#     au premier NULL) — LA MARCHE QUI TUE LA PIÈCE DEV.7 ET PORTE LA dev.8
def marche_chargeur(rva):
    n, i = 0, 0
    while True:
        e, = struct.unpack_from("<I", donnees, f_rdata(rva) + 4 * i)
        if e == 0:
            return n
        n += 1
        i += 1

comptes = (marche_chargeur(OFT_K32), marche_chargeur(OFT_U32),
           marche_chargeur(OFT_GDI), marche_chargeur(OFT_DEMO))
print(f"LA MARCHE DU CHARGEUR sur la pièce retouchée : "
      f"{comptes[0]} · {comptes[1]} · {comptes[2]} · {comptes[3]}")
assert comptes == (10, 18, 6, 3), "la marche du chargeur != le plan"

# 4b. chaque entrée pointe un hint/nom valide (WORD hint + nom ASCII NUL)
def nom_de(e):
    fo = f_rdata(e)
    fin = donnees.find(b"\0", fo + 2)
    return bytes(donnees[fo + 2:fin]).decode("ascii")

tous = [e for arr in (k32, u32, gdi, demo) for e in arr]
for e in tous:
    nm = nom_de(e)
    assert nm and all(33 <= ord(c) < 127 for c in nm), f"nom invalide @ {e:#x}"
print(f"les {len(tous)} hint/noms relus : "
      f"{nom_de(tous[0])} … {nom_de(tous[-1])}")

# 4c. les régions INTACTES : .text, .text2, .data, en-têtes, descripteurs,
#     hint/noms, IAT FT — la retouche ne touche QUE 0x28A0-0x2A00 + 0x2E80
origine = open(SRC, "rb").read()
diffs = [i for i in range(len(donnees)) if donnees[i] != origine[i]]
plages_modifiees, debut = [], None
for i in range(len(donnees) + 1):
    if i < len(donnees) and donnees[i] != origine[i]:
        if debut is None:
            debut = i
    elif debut is not None:
        plages_modifiees.append((debut, i - 1))
        debut = None
print(f"octets modifiés : {len(diffs)} — plages fichier : "
      f"{[(hex(a), hex(b)) for a, b in plages_modifiees]}")
for a, b in plages_modifiees:
    rva_a = a - 0x1200 + 0x2000 if a >= 0x1200 else a
    rva_b = b - 0x1200 + 0x2000 if b >= 0x1200 else b
    dans_rdata_of = 0x28A0 <= rva_a and rva_b < 0x2A00
    dans_version = rva_a == rva_b == R_VERSION
    assert dans_rdata_of or dans_version, \
        f"MODIFICATION HORS ZONE PRÉVU : rva {rva_a:#x}-{rva_b:#x}"
print("la retouche confinée : OFT 0x28A0-0x2A00 + le qword version — "
      "TOUT LE RESTE OCTET-IDENTIQUE")

# 4d. les têtes scellées et l'IAT FT inchangées (les constantes du scénario)
TETES = ((0x1100, bytes.fromhex("57564889c848")),   # memcpy M1
         (0x1180, bytes.fromhex("31c04d85c074")),   # memcmp M1
         (0x13C0, bytes.fromhex("53574889cb48")),   # memset M1
         (0x15C0, bytes.fromhex("534154415541")),   # la boucle démo
         (0xC000, bytes.fromhex("c70167e6096a")))   # sha256-init M9
for rva, attendu in TETES:
    if rva >= 0x4000:                    # .text2
        fo = 0x3200 + (rva - 0x4000)
    elif rva >= 0x1000:                  # .text
        fo = 0x200 + (rva - 0x1000)
    assert bytes(donnees[fo:fo + len(attendu)]) == attendu, \
        f"la tête scellée @{rva:#x} a bougé !"
for i in range(0, 0x148, 8):                    # l'IAT FT
    rva = 0x3100 + i
    fo = f_rdata(rva)
    q, = struct.unpack_from("<Q", origine, fo)
    q2, = struct.unpack_from("<Q", donnees, fo)
    assert q == q2, f"le slot FT @{rva:#x} a changé !"
print("les têtes scellées et les 41 slots FT : INTACTS")

import os
os.makedirs("/home/z/my-project/build-dev10", exist_ok=True)
open(DST, "wb").write(bytes(donnees))
sha = hashlib.sha256(bytes(donnees)).hexdigest()
md5 = hashlib.md5(bytes(donnees)).hexdigest()
print(f"\nLA PIÈCE dev.8 NÉE : {DST}")
print(f"  taille {len(donnees)} o (constante)")
print(f"  sha256 {sha}")
print(f"  md5    {md5}")
