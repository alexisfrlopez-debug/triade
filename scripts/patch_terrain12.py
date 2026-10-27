#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.12 — LA DÉMO PUBLIQUE FINALE EMBARQUÉE (D64, 28/10).

LE RUN 22:10 (terrain_20261027_221053.txt) A FERMÉ T2 : le proxy corrigé
(http-10:R3, probing de pile) a rendu S22/S24 code=0, 640/577 octets,
journal proxy 7 lignes, S28 VERDICT OK — correctif D63 CONFIRMÉ par
expérience contrôlée (seule variable changée terrain.10→11 : le proxy).

T1, LUI, EST UN SUCCÈS MASQUÉ PAR L'OUTIL DE MESURE :
  - la démo diagnostique embarquée (demo10, cf72462d) va AU BOUT — preuve :
    demo_journal.txt du run 18:00 (déposé sur Drive) : 28 lignes, fin
    « retour arrière : identité confirmée » + « boucle § 5 complète - DÉMO OK » ;
  - le superviseur attend 17 lignes (le journal de la démo PUBLIQUE demo.9,
    D43 : 6 lignes L* + 11 lignes J_* de win-09:R4) — 28 ≠ 17 → KO STRUCTUREL ;
  - et le superviseur lit au plus MAX_LECTURE = 640 o (layout.py:630) : le
    journal diagnostique en fait 706 → tronqué à 640, coupant PILE dans
    « retour arrière » (octets 639-640 = « re ») — le fragment « re » des
    runs 19:23/21:38/22:10 est la SIGNATURE de cette troncature (3 fois le
    même octet de coupure).

LE CORRECTIF (data-only, un seul changement) : embarquer demo.9 PUBLIQUE
(md5 73c064fbaf4610a167bc6434dee400e4, MÊME TAILLE 16 384 o — in-place)
à la place de demo10-diagnostique. Le superviseur est INCHANGÉ : son
verdict T1 (exit 0 ET 17 lignes ET 31 derniers octets == « boucle § 5
complète - DÉMO OK\r\n » cp1252) correspond EXACTEMENT au journal de
demo.9 — vérifié statiquement (scripts/journal_attendu_demo9.py) :
17 lignes, 519 o < 640, marqueur final == FIX_FINAL_DEMO.

CE PATCH (terrain.11 → terrain.12) :
  1. BLOB_DEMO @0x6410 (rva 0x8010) : demo10-diagnostique remplacé
     IN-PLACE par demo.9 (16 384 o, aucun décalage) ;
  2. la chaîne md5 S04C (@0x585F, rva 0x6A5F) mise à jour ;
  3. génération terrain11 → terrain12 (L00/S00), VERSIONINFO 0.5.12.0,
     FileVersion « 0.5.12 », ProductVersion « …terrain12 » ;
  4. sommes R10[23] (S00), R10[25] (chaînes md5), R10[26] (kit entier)
     recalculées.
Le superviseur LUI-MÊME (fenêtre, scénario, verdicts, sup-34 ABI-conforme,
proxy 0.4.0-dev.2) reste INCHANGÉ — la seule variable est la démo embarquée.

T3 (OAuth ÉCHEC à chaque run) reste OUVERT — la pièce terrain_jeton.json
(réponse OAuth, SANS secret) est demandée au terrain via le LISEZMOI.
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain11.exe"
DST = REPO / "terrain/livraison/superviseur-terrain12.exe"
DEMO9 = REPO / "demo/demo.exe"
DEMO10 = REPO / "demo/livraison/demo10-diagnostique.exe"

MD5_TERRAIN11 = "96ac3abff2f7d726e1a8ac18e17d2ebb"
MD5_DEMO9 = b"73c064fbaf4610a167bc6434dee400e4"
MD5_DEMO10 = b"cf72462dc130aa4753a2fe5e78f06a08"

R10_TABLE_RVA = 0x2450
OFF_DEMO = 0x6410            # offset fichier de BLOB_DEMO (rva 0x8010)
TAILLE_DEMO = 0x4000         # 16 384 o
OFF_MD5_DEMO = 0x585F        # offset fichier de la chaîne md5 S04C (rva 0x6A5F)
OFF_ENETE_KIT = (0x6400, 0x6410)      # en-tête kit : u64 démo + u64 proxy
OFF_PROXY = 0xA410           # début du proxy embarqué (inchangé)
OFF_ANNEXE = 0xF010          # début du slot annexe jetons (inchangé)


def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1400 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if 0x4000 <= rva < 0x6E00:
        return 0x2E00 + (rva - 0x4000)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None


def somme_zone(data, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def lire_table(data):
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k, table_off
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur")


def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)


# =============================================================================
# 1. GARDES-FOUS
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN11:
    erreur("terrain.11 : md5 inattendu")

demo9 = DEMO9.read_bytes()
if len(demo9) != TAILLE_DEMO:
    erreur(f"demo.9 : {len(demo9)} o != {TAILLE_DEMO} (in-place impossible)")
if hashlib.md5(demo9).hexdigest() != MD5_DEMO9.decode():
    erreur("demo.9 : md5 inattendu (rebuild démo ?)")

# la démo diagnostique in-place, octets exacts
demo10 = DEMO10.read_bytes()
if bytes(base[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo10:
    erreur("demo10-diagnostique introuvable @0x6410 (kit déplacé ?)")
# la chaîne md5 v10 en place
if bytes(base[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO10:
    erreur("chaîne md5 S04C : demo10 introuvable @0x585F")

# versions courantes = 11 / terrain.11
OFF_L00 = rva2off(0x2ADA)      # dernier caractère de L00
OFF_S00 = rva2off(0x4366)      # dernier caractère de S00
if bytes(base[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain11" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if bytes(base[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain11" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", base, off_b)[0] != 11:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 11")
if base[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.11":
    erreur(f"FileVersion inattendue : {base[0x5DB8:0x5DC8].decode('utf-16-le', 'replace')!r}")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain11":
    erreur(f"ProductVersion (fin) inattendue : {base[0x5EC0:0x5ECE].decode('utf-16-le', 'replace')!r}")

# le correctif ABI terrain.10 en place (le superviseur ne change pas)
if bytes(base[rva2off(0x5D1E):rva2off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("sup-34 .curl : correctif D62 absent (48 83 ec 28 attendu)")

# la table : 27 entrées + terminateur, toutes vertes sur terrain.11
entrees, idx_term, table_off = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.11 : R10[{k}] ROUGE avant patch")

# couvreurs des zones touchées : S00 (R10[23]), chaîne md5 démo (R10[25]),
# zone démo du kit (R10[26])
zones = [("démo (kit)", 0x8010, TAILLE_DEMO),
         ("chaîne md5 démo", 0x6A5F, 32),
         ("S00", 0x4365, 2)]
attendus = {"démo (kit)": {26}, "chaîne md5 démo": {25}, "S00": {23}}
for lab, zrva, zln in zones:
    cov = {k for k, (rva, ln, sm) in enumerate(entrees)
           if not (rva + ln <= zrva or zrva + zln <= rva)}
    if cov != attendus[lab]:
        erreur(f"couvreurs de {lab} : {sorted(cov)} != {sorted(attendus[lab])}")
    print(f"[couv] {lab} couvert par R10{sorted(cov)}")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# (a) LA DÉMO PUBLIQUE, in-place dans le kit embarqué
img[OFF_DEMO:OFF_DEMO + TAILLE_DEMO] = demo9

# (b) la chaîne md5 S04C
img[OFF_MD5_DEMO:OFF_MD5_DEMO + 32] = MD5_DEMO9

# (c) génération : terrain11 -> terrain12 (dernier caractère)
img[OFF_L00] = ord("2")
img[OFF_S00] = ord("2")

# (d) VERSIONINFO binaire 0.5.12.0
struct.pack_into("<H", img, 0x5CD4, 12)
struct.pack_into("<H", img, 0x5CDC, 12)

# (e) chaîne FileVersion « 0.5.11 » -> « 0.5.12 » (utf-16, dernier char)
img[0x5DC2:0x5DC4] = "2".encode("utf-16-le")

# (f) chaîne ProductVersion « …terrain11 » -> « …terrain12 » (dernier char)
img[0x5ECC:0x5ECE] = "2".encode("utf-16-le")

# (g) sommes R10[23], R10[25], R10[26] recalculées sur l'image finale
for k in (23, 25, 26):
    rva_k, ln_k, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(img, rva_k, ln_k))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné (démo + md5 + génération + .rsrc + 3 sommes)
autorisations = [
    (OFF_DEMO, OFF_DEMO + TAILLE_DEMO, "démo.9 in-place"),
    (OFF_MD5_DEMO, OFF_MD5_DEMO + 32, "chaîne md5 S04C"),
    (OFF_L00, OFF_L00 + 1, "L00"),
    (OFF_S00, OFF_S00 + 1, "S00"),
    (0x5CD4, 0x5CD6, "bin1"), (0x5CDC, 0x5CDE, "bin2"),
    (0x5DC2, 0x5DC4, "FV"), (0x5ECC, 0x5ECE, "PV"),
    (table_off + 16 * 23 + 8, table_off + 16 * 23 + 16, "somme R10[23]"),
    (table_off + 16 * 25 + 8, table_off + 16 * 25 + 16, "somme R10[25]"),
    (table_off + 16 * 26 + 8, table_off + 16 * 26 + 16, "somme R10[26]"),
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs
        if not any(a <= i < b for a, b, _ in autorisations)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous bornés "
      f"(démo ~{sum(1 for i in diffs if OFF_DEMO <= i < OFF_DEMO + TAILLE_DEMO)} + md5 32 + génération 2 + .rsrc 6 + sommes 24)")

# 3b. la porte ENTIÈRE verte + terminateur
entrees_f, idx_term_f, _ = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
if struct.unpack_from("<IIQ", img, table_off + 16 * 27) != (0, 0, 0):
    erreur("le terminateur a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. le kit embarqué : en-tête + proxy + annexe INTACTS, démo == demo.9
if img[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]] != base[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]]:
    erreur("l'en-tête kit (longueurs) a bougé")
if img[OFF_PROXY:OFF_ANNEXE] != base[OFF_PROXY:OFF_ANNEXE]:
    erreur("le proxy embarqué a bougé")
if img[OFF_ANNEXE:] != base[OFF_ANNEXE:]:
    erreur("l'annexe jetons a bougé")
if bytes(img[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo9:
    erreur("la démo embarquée != demo/demo.exe")
print("[blob] en-tête kit + proxy 0.4.0-dev.2 + annexe jetons inchangés ; "
      "démo embarquée == demo.9 (md5 73c064fb…) octet pour octet")

# 3d. le md5 S04C journalisé
if bytes(img[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO9:
    erreur("md5 S04C final inattendu")
print("[md5] S04C journalisera 73c064fbaf4610a167bc6434dee400e4")

# 3e. identité
if bytes(img[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain12" or bytes(img[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain12":
    erreur("versions L00/S00 finales inattendues")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", img, off_b)[0] != 12:
        erreur(f"VERSIONINFO finale inattendue @{off_b:#x}")
fv = img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0]
if fv != "0.5.12":
    erreur(f"FileVersion finale inattendue : {fv!r}")
pv = img[0x5EC0:0x5ECE].decode("utf-16-le")
if pv != "rrain12":
    erreur(f"ProductVersion (fin) inattendue : {pv!r}")
print("[ident] L00/S00 « terrain12 », VERSIONINFO 0.5.12.0, "
      "FileVersion « 0.5.12 », ProductVersion « …terrain12 »")

# 3f. le prologue du proxy embarqué inchangé (le probing D63, désassemblé)
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    off_pro = OFF_PROXY + 0x2C00 + (0x5580 - 0x4000)
    code = bytes(img[off_pro:off_pro + 0x40])
    obtenu = [f"{i.mnemonic} {i.op_str}".rstrip() for i in md.disasm(code, 0x140005580)]
    attendu = [
        "push rbx", "push r12", "push r13", "push r14", "push r15",
        "mov r10, 0xfffffffffffff000",
        "mov rax, qword ptr [rsp + r10]",
        "sub r10, 0x1000",
        "cmp r10, -0x7000",
        "jge 0x140005590",
        "mov rax, qword ptr [rsp - 0x7100]",
        "sub rsp, 0x7100",
    ]
    if obtenu[:12] != attendu:
        erreur("prologue http-10 embarqué inattendu (proxy altéré ?)")
    print("[code] prologue http-10 embarqué intact : push×5 ; BOUCLE DE "
          "PROBING ; sub rsp,0x7100")
except ImportError:
    print("[code] capstone absent (FAIBLE)")

# 3g. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
