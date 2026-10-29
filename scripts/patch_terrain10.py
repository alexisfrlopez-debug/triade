#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.10 — LE CORRECTIF DU TUEUR DE T2 (D62, 27/10 au soir).

LE VERDICT DU RUN 20:47 (terrain_20261027_204700.txt, 884 o) + LA CAPTURE
DE L'HISTORIQUE DE PROTECTION (20:51:30) RENVERSENT L'ENQUÊTE :
  - AUCUNE entrée Defender aux instants des morts (19:23, 20:01, 20:47) ;
    les seules actions Defender du jour : 12:55 (quarantaine proxy.exe),
    16:48-16:50 (bloquée/restaurée/réparation incomplète, AVANT terrain.5),
    20:50 (falsifications + échantillons désactivés — APRÈS le run : la
    coupure D60 n'a PAS été appliquée pendant le run, l'expérience est
    caduque). DEFENDER EST INNOCENT DES MORTS AU CURL.
  - L'anomalie T1 inédite (S13 code=259 = STILL_ACTIVE + S14 lignes=0) :
    paire COHÉRENTE — le demo vivait encore (journal verrouillé share=0 →
    lecture vide) ; le bind a réussi (sinon tcp-12 E1 l'aurait tué code=2),
    donc ralentissement ou gel du scénario demo — demo_journal.txt du run
    non déposé, pièce demandée.
  - L'ARME DU CRIME, TROUVÉE PAR AUDIT ABI (scripts/audit_shadow_sup34.py,
    méthode D41) : le sous-bloc .curl de sup-34 (@0x5d1e) appelle
    WaitForSingleObject (@0x5d3c, rdx=25000), GetExitCodeProcess (@0x5d4c,
    rdx=&ETAT_SUP) et CloseHandle (@0x5d55) avec D=0x8 — AUCUN shadow space
    (sub rsp,8 seul). Ces 4 défauts étaient DOCUMENTÉS par D53 (« réels
    mais PAS le tueur pré-fenêtre ») puis oubliés : or le tueur actuel est
    EXACTEMENT là. Mécanique (prouvée sur CETTE machine par demo.6/D41 —
    kernel32 /homeparams range rdx dans [rsp+0x10]) : le spill écrase
    l'adresse de retour de .curl → ret vers 0x61a8 ou une adresse .data →
    c0000005 exécution page NX → processus mort, fenêtre fermée, journal
    coupé AVANT S22 (journalisé après le retour de .curl) — la signature
    EXACTE des 4/4 morts, et la famille des 15 rapports WER BEX64 de
    l'ère terrain.1-3. Cohérence interne parfaite : tous les sites sains
    (sup-33, sup-35, corps de sup-34) ont TOUJOURS survécu ; seuls les
    sites D=0x8 tuent.

LE CORRECTIF (2 octets, ABI msx64) :
  sub rsp,8  → sub rsp,0x28  (@0x5d21 : 08→28)
  add rsp,8  → add rsp,0x28  (@0x5d63 : 08→28)
D=0x28 aux quatre appels de .curl (les 3 IAT + l'appel direct sup-31) ;
alignement préservé (0x28 ≡ 8 mod 16) ; l'adresse de retour sort de la
zone d'accueil de la callee. Le `je 0x5d60` converge vers le nouvel épilogue.

Génération : L00/S00 « terrain10 » (9 octets — le point saute à partir de
la génération 10, place fixe), VERSIONINFO binaire 0.5.10.0, chaîne
FileVersion « 0.5.10 » (6 cars, NUL dans le slot des 7), ProductVersion
« …terrain10 ». Sommes R10[20] (couvre 0x5d21/0x5d63) et R10[23] (couvre
S00) recalculées — table relue JUSQU'AU TERMINATEUR (méthode D56).

LATENTS DOCUMENTÉS (NON corrigés cette itération — une variable par
itération, chemins jamais exécutés ou callee maison) :
  - sup-31 @0x5382 : CloseHandle du nettoyage tuyaux en échec mode 1
    (jamais exécuté en 4+ runs) ;
  - sup-34 @0x5d65 : aide journal (callee = win-05, code maison sans
    spill homeparams).
  File d'attente M8 : correction notation.
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain9.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain10.exe")

MD5_TERRAIN9 = "a59931db4e3bfc14a29e927a79cc73ca"

RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if RDATA_RVA <= rva < 0x3000:
        return RDATA_FILE + (rva - RDATA_RVA)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if TEXT2_RVA <= rva < 0x6E00:
        return TEXT2_FILE + (rva - TEXT2_RVA)
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
            return entrees, k
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
if hashlib.md5(base).hexdigest() != MD5_TERRAIN9:
    erreur("terrain.9 : md5 inattendu")

# le sous-bloc .curl défectueux, octets exacts AVANT correctif
OFF_SUB = rva2off(0x5D1E)
OFF_ADD = rva2off(0x5D60)
if bytes(base[OFF_SUB:OFF_SUB + 4]) != bytes.fromhex("4883ec08"):
    erreur(".curl @0x5d1e : « sub rsp,8 » attendu (48 83 ec 08)")
if bytes(base[OFF_ADD:OFF_ADD + 5]) != bytes.fromhex("4883c408c3"):
    erreur(".curl @0x5d60 : « add rsp,8 ; ret » attendu (48 83 c4 08 c3)")
if base[OFF_SUB + 4:OFF_SUB + 6] != bytes.fromhex("31d2"):
    erreur(".curl @0x5d22 : « xor edx,edx » attendu")
if struct.unpack_from("<H", base, OFF_SUB + 0x19 - 0x1E + OFF_SUB)[0]:  # noqa
    pass
# le motif mov edx,25000 ; call [rip] (l'ancre du diagnostic D61)
if bytes(base[rva2off(0x5D37):rva2off(0x5D37) + 7]) != bytes.fromhex("baa8610000ff15"):
    erreur(".curl @0x5d37 : motif « mov edx,25000 ; call » absent")

# versions courantes = 9 / terrain.9
OFF_L00 = rva2off(0x2ADA)
OFF_S00 = rva2off(0x4366)
if base[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.9" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if base[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.9" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b, off_s in ((0x5CD4, 0x5DC4), (0x5CDC, 0x5ECC)):
    if struct.unpack_from("<H", base, off_b)[0] != 9:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 9")
    if base[off_s:off_s + 2] != "9".encode("utf-16-le"):
        erreur(f"VERSIONINFO chaîne @{off_s:#x} != '9'")
# chaîne FileVersion « 0.5.0.9 » @0x5DB8 (utf-16), ProductVersion finit « terrain.9 »
if base[0x5DB8:0x5DC6].decode("utf-16-le") != "0.5.0.9":
    erreur(f"FileVersion inattendue : {base[0x5DB8:0x5DC6].decode('utf-16-le', 'replace')!r}")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain.9":
    erreur(f"ProductVersion (fin) inattendue : {base[0x5EC0:0x5ECE].decode('utf-16-le', 'replace')!r}")

# le correctif FindWindowW de terrain.6 en place
OFF_SUP33 = rva2off(0x544F)
if bytes(base[OFF_SUP33:OFF_SUP33 + 9]) != bytes.fromhex("488d0d3cd6ffff31d2"):
    erreur("sup-33 @0x544f : correctif FindWindowW absent")

# la table : 27 entrées + terminateur, toutes vertes sur terrain.9
table_off = rva2off(R10_TABLE_RVA)
entrees, idx_term = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.9 : R10[{k}] ROUGE avant patch")

# quelles entrées couvrent les octets qu'on va toucher ?
touches = [(0x5D21, 1, "sub rsp,0x28 (LE CORRECTIF)"),
           (0x5D63, 1, "add rsp,0x28 (LE CORRECTIF)"),
           (0x2AD9, 2, "L00 « terrain10 »"),
           (0x4365, 2, "S00 « terrain10 »"),
           (0x70D4, 2, "VERSIONINFO bin 1"), (0x70DC, 2, "VERSIONINFO bin 2"),
           (0x71C0, 2, "FileVersion s1"), (0x71C2, 2, "FileVersion s2"),
           (0x71C4, 2, "FileVersion s3"),
           (0x72CA, 2, "ProductVersion s1"), (0x72CC, 2, "ProductVersion s2")]
couvreurs = set()
for k, (rva, ln, sm) in enumerate(entrees):
    for (arva, aln, lab) in touches:
        if not (rva + ln <= arva or arva + aln <= rva):
            print(f"[couv] R10[{k}] (rva={rva:#x} len={ln:#x}) couvre {lab}")
            couvreurs.add(k)
if couvreurs != {20, 23}:
    erreur(f"couvreurs {sorted(couvreurs)} != {{20, 23}} attendus")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# (a) LE CORRECTIF ABI — 2 octets
img[rva2off(0x5D21)] = 0x28            # sub rsp, 0x28
img[rva2off(0x5D63)] = 0x28            # add rsp, 0x28

# (b) génération : terrain.9 -> terrain10 (le point saute, place fixe de 9)
img[OFF_L00 - 1] = ord("1"); img[OFF_L00] = ord("0")
img[OFF_S00 - 1] = ord("1"); img[OFF_S00] = ord("0")

# (c) VERSIONINFO binaire 0.5.10.0
struct.pack_into("<H", img, 0x5CD4, 10)
struct.pack_into("<H", img, 0x5CDC, 10)

# (d) chaîne FileVersion « 0.5.0.9 » -> « 0.5.10 » (NUL dans le slot des 7)
img[0x5DC0:0x5DC2] = "1".encode("utf-16-le")
img[0x5DC2:0x5DC4] = "0".encode("utf-16-le")
img[0x5DC4:0x5DC6] = "\x00".encode("utf-16-le")

# (e) chaîne ProductVersion « …terrain.9 » -> « …terrain10 »
img[0x5ECA:0x5ECC] = "1".encode("utf-16-le")
img[0x5ECC:0x5ECE] = "0".encode("utf-16-le")

# (f) sommes R10[20] et R10[23] recalculées sur l'image finale
for k in (20, 23):
    rva_k, ln_k, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(img, rva_k, ln_k))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné (2 correctif + 4 génération + 10 .rsrc + 16 sommes)
autorisations = [
    (rva2off(0x5D21), rva2off(0x5D21) + 1, "sub"),
    (rva2off(0x5D63), rva2off(0x5D63) + 1, "add"),
    (OFF_L00 - 1, OFF_L00 + 1, "L00"),
    (OFF_S00 - 1, OFF_S00 + 1, "S00"),
    (0x5CD4, 0x5CD6, "bin1"), (0x5CDC, 0x5CDE, "bin2"),
    (0x5DC0, 0x5DC6, "FV str"), (0x5ECA, 0x5ECE, "PV str"),
    (table_off + 16 * 20 + 8, table_off + 16 * 20 + 16, "somme R10[20]"),
    (table_off + 16 * 23 + 8, table_off + 16 * 23 + 16, "somme R10[23]"),
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs
        if not any(a <= i < b for a, b, _ in autorisations)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
n_par = {lab: sum(1 for i in diffs if any(a <= i < b for a, b, lab2 in autorisations
                                          if lab2 == lab and a <= i < b))
         for _, _, lab in [(0, 0, l) for _, _, l in autorisations]}
print(f"[diff] {len(diffs)} octets modifiés, tous bornés : "
      f"2 correctif + {sum(1 for i in diffs if any(a <= i < b for a, b, l in autorisations if l in ('L00','S00')))} génération "
      f"+ .rsrc + 16 sommes")

# 3b. la porte ENTIÈRE verte + terminateur
entrees_f, idx_term_f = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
if struct.unpack_from("<IIQ", img, table_off + 16 * 27) != (0, 0, 0):
    erreur("le terminateur a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. le .curl corrigé, désassemblé
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    code = bytes(img[rva2off(0x5D1E):rva2off(0x5D1E) + 0x47])
    attendu = [
        "sub rsp, 0x28", "xor edx, edx",
        "call 0x140005200", "test eax, eax", "je 0x140005d60",
        "mov r12, qword ptr [rip - 0x2224]", "mov rcx, r12",
        "mov edx, 0x61a8", "call qword ptr [rip - 0x3a32]",
        "mov rcx, r12", "lea rdx, [rip - 0x21fc]",
        "call qword ptr [rip - 0x3a3a]",
        "mov rcx, r12", "call qword ptr [rip - 0x3c63]",
        "mov eax, 1", "add rsp, 0x28", "ret",
    ]
    obtenu = [f"{i.mnemonic} {i.op_str}".rstrip()
              for i in md.disasm(code, 0x140005D1E)]
    if obtenu != attendu:
        for i, (a, b) in enumerate(zip(obtenu, attendu)):
            if a != b:
                print(f"  divergence @{i}: {a!r} != {b!r}")
        erreur(f"désassemblage .curl inattendu ({len(obtenu)} instr)")
    print("[code] .curl : sub rsp,0x28 ; 3 appels IAT ; add rsp,0x28 ; ret —"
          " shadow space 0x20 + retour, ABI CONFORME")
except ImportError:
    print("[code] capstone absent (FAIBLE)")

# 3d. le kit embarqué inchangé byte pour byte
if img[0x6400:] != base[0x6400:]:
    erreur("le .blob (demo.10 + proxy + annexe jetons) a bougé")
print("[blob] demo.10 + proxy.exe + annexe jetons : inchangés byte pour byte")

# 3e. identité
if img[OFF_L00 - 8:OFF_L00 + 1] != b"terrain10" or img[OFF_S00 - 8:OFF_S00 + 1] != b"terrain10":
    erreur("versions L00/S00 finales inattendues")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", img, off_b)[0] != 10:
        erreur(f"VERSIONINFO finale inattendue @{off_b:#x}")
fv = img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0]
if fv != "0.5.10":
    erreur(f"FileVersion finale inattendue : {fv!r}")
pv = img[0x5EC0:0x5ECE].decode("utf-16-le")
if pv != "rrain10":
    erreur(f"ProductVersion (fin) inattendue : {pv!r}")
print("[ident] L00/S00 « terrain10 », VERSIONINFO 0.5.10.0, "
      "FileVersion « 0.5.10 », ProductVersion « …terrain10 »")

# 3f. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
