#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo.10 — construction du build DIAGNOSTIQUE instrumenté (D57).

LE CONSTAT (2 runs terrain, machine réelle du développeur) :
  terrain.5 (16:52, clic manuel)  : journal demo.9 coupe sur « réseau :
  échange en échec » après « client : connecté ».
  terrain.7 (18:00, clic superviseur BM_CLICK) : MÊME échec — S02 porte
  VERTE, kit conforme, fenêtre détectée, clic envoyé, le demo rejoue
  jusqu'à « client : connecté » puis « réseau : échange en échec »
  (ligne E5 de win-09 : send <= 0 / recv <= 0 / memcmp != 0) — ARRÊT
  PROPRE du scénario (E5 = ligne + nettoyage + arrêt), fenêtre ouverte.

L'ANALYSE STATIQUE EXHAUSTIVE (demo.8 vs demo.9, ce diagnostic) :
  chaîne réseau byte-identique (tcp-01..09, win-07, trampoline, écho v1,
  win-09 phase réseau), win-10 logique identique (5 pushes/5 pops sains),
  init CS D42 vivante, tcp-11 propre, la seule différence = les sondes
  D43 retirées (S1/S2 serveur, sonde4/5 client). L'échec est un fait
  d'exécution INVISIBLE en statique — exactement la classe demo.7 (D42).

LA MÉTHODE DU PROJET (D40-D42, trois fois payante) : INSTRUMENTER.
  demo.10 = demo.8 (l'instrumenté, 28/28 lignes VERTES sur CETTE machine
  le 26/10) + identification de génération. Les sondes S1/S2/sonde4/
  sonde5 encadrent l'intervalle mort exact : S1 (accept revenu ?),
  S2 (fil écho créé ?), sonde4 (émission complète ?), sonde5 (réception
  complète ?) — la dernière sonde visible localise la mort à
  l'instruction près, et le verdict memcmp tranche la divergence de
  contenu. demo.8 est repris BYTE POUR BYTE (aucune reconstruction) :

LE PATCH (3 zones bornées) :
  1. .rdata @rva 0x2ec5 : « demo.8 » -> « demo10 » (6 octets, MÊME
     longueur — la chaîne L00 est à longueur explicite edx=0x28, les
     chaînes sont collées, AUCUN décalage) ;
  2. .rdata @rva 0x2628 : u64 version 0x00030108 -> 0x0003010A ;
  3. sommes R10 des entrées couvrant ces octets, recalculées sur
     l'image finale — table lue JUSQU'AU TERMINATEUR rva==0 (leçon
     D56 : jamais de compte en dur).

POST-VÉRIFICATIONS fail-closed :
  - diff demo.8 -> demo.10 : UNIQUEMENT les 6+1 octets de version et les
    champs de sommes R10 recomputés, RIEN d'autre ;
  - porte R10 : toutes les entrées + terminateur VERTS ;
  - les 4 chaînes de sondes et les blocs win-08:R2/win-09:R3/win-10:R2
    INTACTS byte pour byte (l'instrumentation est le point du build) ;
  - le u64 version >= plancher 0x30000 (0x3010A ✓).
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/tmp/demo8.exe")        # demo.8 terrain-vert (md5 64ed490e…)
DST = pathlib.Path("/home/z/my-project/triade/demo/livraison/demo10-diagnostique.exe")

MD5_DEMO8 = "64ed490e4d5af77952a40a686a3ae40c"

R10_TABLE_RVA = 0x2450

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x200 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1200 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        return 0x2200 + (rva - 0x3000)
    if 0x4000 <= rva < 0x5400:
        return 0x2C00 + (rva - 0x4000)
    return None

def somme_zone(data, rva, ln):
    """Somme tronquée de mots u64 LE — l'algorithme exact de la porte (win-06)."""
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

def lire_table(data):
    """Entrées jusqu'au TERMINATEUR rva==0 — la vraie boucle de la porte."""
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur")

def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)

# =============================================================================
# 1. GARDES-FOUS sur demo.8
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(base).hexdigest() != MD5_DEMO8:
    erreur("demo.8 : md5 inattendu")

OFF_L00 = rva2off(0x2ECA)
if base[OFF_L00:OFF_L00 + 6] != b"demo.8":
    erreur(f"L00 @0x2eca : {bytes(base[OFF_L00:OFF_L00+6])!r} != 'demo.8'")
# le contexte : « L00 demarrage demonstration 0.3.0-demo.8 » puis « L01 »
if base[OFF_L00 - 34:OFF_L00] != b"L00 demarrage demonstration 0.3.0-":
    erreur("L00 : contexte inattendu")
if base[OFF_L00 + 6:OFF_L00 + 9] != b"L01":
    erreur("L00 : la chaîne suivante n'est pas L01 (géométrie collée attendue)")

if struct.unpack_from("<Q", base, rva2off(0x2628))[0] != 0x30108:
    erreur("u64 version @0x2628 != 0x30108")

# la table : toutes les entrées VERTES sur demo.8, lues au terminateur
entrees, idx_term = lire_table(base)
print(f"[pre] table R10 : {idx_term} entrées + terminateur")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"demo.8 : R10[{k}] ROUGE avant patch — base corrompue ?")

# les 4 chaînes de sondes présentes (l'instrumentation EST le build) —
# chaînes collées à longueur explicite (12+17+16+14, un \0 final), D40/D42
for off_att, attendu in ((rva2off(0x266E), b"S1 accept ok"),
                         (rva2off(0x267A), b"S2 fil echo lance"),
                         (rva2off(0x268B), b"sonde4 envoye ok"),
                         (rva2off(0x269B), b"sonde5 recu ok")):
    if bytes(base[off_att:off_att + len(attendu)]) != attendu:
        erreur(f"chaîne sonde manquante @rva {off_att:#x}")

# quelles entrées couvrent les octets qu'on va toucher ?
touches = [(0x2ECA, 6, "L00 'demo10'"), (0x2628, 8, "u64 version 0x3010A")]
couvreurs = set()
for k, (rva, ln, sm) in enumerate(entrees):
    for (arva, aln, lab) in touches:
        if not (rva + ln <= arva or arva + aln <= rva):
            print(f"[couv] R10[{k}] (rva={rva:#x} len={ln:#x}) couvre {lab}")
            couvreurs.add(k)

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)
img[OFF_L00:OFF_L00 + 6] = b"demo10"                      # 6 octets, même taille
struct.pack_into("<Q", img, rva2off(0x2628), 0x3010A)     # u64 version

# sommes R10 des entrées couvrantes, recalculées sur l'image finale
table_off = rva2off(R10_TABLE_RVA)
for k in sorted(couvreurs):
    rva, ln, _ = entrees[k]
    nouvelle = somme_zone(img, rva, ln)
    struct.pack_into("<Q", img, table_off + 16 * k + 8, nouvelle)

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff : uniquement version + sommes autorisées
autorise = [(OFF_L00, OFF_L00 + 6), (rva2off(0x2628), rva2off(0x2628) + 8)]
for k in sorted(couvreurs):
    autorise.append((table_off + 16 * k + 8, table_off + 16 * k + 16))
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorise)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés (version + {len(couvreurs)} somme(s) R10), tous bornés")

# 3b. la porte ENTIÈRE verte + terminateur intact
entrees_f, idx_term_f = lire_table(img)
if idx_term_f != idx_term:
    erreur(f"table finale : {idx_term_f} entrées != {idx_term}")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
term = struct.unpack_from("<IIQ", img, table_off + 16 * idx_term)
if term != (0, 0, 0):
    erreur("le terminateur a bougé")
print(f"[porte] R10 : {idx_term}/{idx_term} entrées VERTES + terminateur intact")

# 3c. l'instrumentation intacte byte pour byte
for rva1, rva2 in ((0x1D00, 0x1E00),   # win-08:R2 (S1/S2)
                   (0x4980, 0x4C00),   # win-10:R2 (sonde4/5)
                   (0x4C00, 0x5000)):  # win-09:R3 (sonde1/2/3)
    if img[rva2off(rva1):rva2off(rva2)] != base[rva2off(rva1):rva2off(rva2)]:
        erreur(f"bloc [{rva1:#x}..{rva2:#x}] modifié — l'instrumentation doit être INTACTE")
print("[instr] win-08:R2, win-09:R3, win-10:R2 : intacts byte pour byte")

# 3d. la nouvelle identité
verif_l00 = bytes(img[OFF_L00 - 34:OFF_L00 + 9])
if not verif_l00.startswith(b"L00 demarrage demonstration 0.3.0-demo10"):
    erreur(f"L00 final inattendu : {verif_l00!r}")
u64 = struct.unpack_from("<Q", img, rva2off(0x2628))[0]
if u64 != 0x3010A or u64 < 0x30000:
    erreur(f"u64 version final : {u64:#x}")
print(f"[ident] L00 = 'L00 demarrage demonstration 0.3.0-demo10' ; u64 {u64:#x}")

# 3e. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
if len(img) != 16384:
    erreur(f"taille {len(img)} != 16384 (le slot .blob du superviseur est fixe)")
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
