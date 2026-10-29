#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.11 — LE PROXY CORRIGÉ EMBARQUÉ (D63, 27/10 au soir).

LE RUN 21:38 (terrain_20261027_213813.txt, 1 932 o) EST LE PREMIER RUN
COMPLET DE L'HISTOIRE : terrain.10 a SURVÉCU au curl (le correctif ABI D62
est CONFIRMÉ — S22 rendu, scénario jusqu'à S91 + nettoyage S07). Mais :
  - T2 KO : curl http code=56, https code=7, journal proxy 1 ligne (la
    bannière seule — aucun « connexion entrante », aucun « arret ») ;
  - T3 KO : jeton OAuth ÉCHEC (S33) — curl DIRECT (sup-35:Q3), cause
    encore ouverte (réseau sortant ? jetons ?) ;
  - T1 KO : S15/S16 — divergence 26≠17 DÉJÀ documentée (non corrigée
    cette itération : une variable par itération).

L'ARME DU CRIME T2, TROUVÉE AU BINAIRE (scripts/diag_prologue_http10.py,
scripts/diag_cadres_m3.py) : le thread session http-10 du proxy fait
  push×5 ; sub rsp, 0x7100 ; … mov [rsp+0x20], 0
dans un thread neuf. Le PE du proxy declare SizeOfStackCommit = 0x1000 :
UNE SEULE PAGE committée à la naissance du thread, guard page dessous. La
première écriture au bas du cadre saute la guard → c00000fd (stack
overflow) → mort DU PROCESSUS ENTIER (une exception de thread tue tout).
Signature EXACTE du run : bannière sortie (thread principal, petit cadre),
puis RST au client (curl 56), port libéré (curl suivant 7), tuyau muet
(S26=1), jamais d'« arret » (le thread console meurt avec le processus).
Le défaut était INVISIBLE : l'oracle unicorn mappe la pile entière (pas
de guard page), le fil echo M2 (réel, démo) avait un cadre de 0x28 o, et
le proxy n'a JAMAIS été exécuté en réel avant le terrain (étape c « sur
le terrain », journal 37/38). Audit ABI du proxy : 0 défaut shadow space
sur 33 sites — le tueur n'était PAS un défaut d'appel IAT mais de PILE.

LE CORRECTIF (côté m3, chaîne complète écrite-avant-code) :
  spec http-10:R3 (P3 réécrite : commit initial 0x1000, guard page ;
  Q0 : boucle de probing ; V6 : contrôle du probing ; historique D63) ;
  brouillon + notation régénérés (1847 o, padding 201 ≥ 16, round-trip
  385/385) ; build_m3 oracle VERT (153 036 cas + falsification détectée,
  R7 : 13 blocs hérités octet-identiques) ; version 0.4.0-dev.2
  (0x00040002, monotonie R10). Le probing (miroir __chkstk) touche
  [rsp-0x1000]…[rsp-0x7000] puis [rsp-0x7100] en descendant — chaque
  touche étend la pile AU PLUS une page sous la zone garantie.

CE PATCH (côté superviseur, terrain.10 → terrain.11, data-only) :
  1. le kit embarqué : proxy.exe 0.4.0-dev.1 (md5 8740e1ca…) remplacé
     IN-PLACE par 0.4.0-dev.2 (md5 dd12b649…, MÊME TAILLE 19 456 o —
     aucun décalage) à l'offset fichier 0xA410 (rva 0xC010) ;
  2. la chaîne md5 S05C embarquée (@0x590A) mise à jour ;
  3. génération terrain10 → terrain11 (L00/S00), VERSIONINFO 0.5.11.0,
     FileVersion « 0.5.11 », ProductVersion « …terrain11 » ;
  4. sommes R10[23] (S00), R10[24] (chaîne md5), R10[26] (le kit entier)
     recalculées.
Le superviseur LUI-MÊME (fenêtre, scénario, verdicts, .curl ABI-conforme)
reste INCHANGÉ — la seule variable de l'itération est le proxy embarqué.
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain10.exe"
DST = REPO / "terrain/livraison/superviseur-terrain11.exe"
PROXY_V2 = REPO / "m3/proxy.exe"

MD5_TERRAIN10 = "ec5995707976b227a5edbab9a766e9b4"
MD5_PROXY_V1 = b"8740e1ca0dbd5967c27cf92bdf713be4"
MD5_PROXY_V2 = b"dd12b64948e64153ff1dd7a66f367ff3"

RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2E00
R10_TABLE_RVA = 0x2450

OFF_PROXY = 0xA410          # offset fichier du proxy dans le kit
TAILLE_PROXY = 0x4C00       # 19 456 o
OFF_MD5 = 0x590A            # offset fichier de la chaîne md5 S05C


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
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN10:
    erreur("terrain.10 : md5 inattendu")

proxy_v2 = PROXY_V2.read_bytes()
if len(proxy_v2) != TAILLE_PROXY:
    erreur(f"proxy v2 : {len(proxy_v2)} o != {TAILLE_PROXY} (in-place impossible)")
if hashlib.md5(proxy_v2).hexdigest() != MD5_PROXY_V2.decode():
    erreur("proxy v2 : md5 inattendu (rebuild m3 ?)")

# le proxy v1 in-place, octets exacts
if bytes(base[OFF_PROXY:OFF_PROXY + TAILLE_PROXY]) != pathlib.Path(
        "/tmp/proxy_dev1.exe").read_bytes():
    erreur("proxy v1 introuvable @0xA410 (kit déplacé ?)")
# la chaîne md5 v1 en place
if bytes(base[OFF_MD5:OFF_MD5 + 32]) != MD5_PROXY_V1:
    erreur("chaîne md5 S05C : v1 introuvable @0x590A")

# versions courantes = 10 / terrain.10
OFF_L00 = rva2off(0x2ADA)      # dernier caractère de L00
OFF_S00 = rva2off(0x4366)      # dernier caractère de S00
if bytes(base[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain10" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if bytes(base[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain10" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", base, off_b)[0] != 10:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 10")
if base[0x5DB8:0x5DC6].decode("utf-16-le") != "0.5.10\x00":
    erreur(f"FileVersion inattendue : {base[0x5DB8:0x5DC6].decode('utf-16-le', 'replace')!r}")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain10":
    erreur(f"ProductVersion (fin) inattendue : {base[0x5EC0:0x5ECE].decode('utf-16-le', 'replace')!r}")

# le correctif ABI terrain.10 en place (le superviseur ne change pas)
if bytes(base[rva2off(0x5D1E):rva2off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("sup-34 .curl : correctif D62 absent (48 83 ec 28 attendu)")

# la table : 27 entrées + terminateur, toutes vertes sur terrain.10
table_off = rva2off(R10_TABLE_RVA)
entrees, idx_term = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.10 : R10[{k}] ROUGE avant patch")

# couvreurs des zones touchées : S00 (R10[23]), md5 (R10[25]), kit (R10[26])
# (la chaîne md5 @off fichier 0x590A vit en .text2 → rva 0x6B0A, couverte
# par R10[25] 0x6A00..0x6E00 — pas R10[24])
zones = [("proxy (kit)", 0xC010, TAILLE_PROXY),
         ("chaîne md5", 0x6B0A, 32),
         ("S00", 0x4365, 2)]
attendus = {"proxy (kit)": {26}, "chaîne md5": {25}, "S00": {23}}
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

# (a) LE PROXY CORRIGÉ, in-place dans le kit embarqué
img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY] = proxy_v2

# (b) la chaîne md5 S05C
img[OFF_MD5:OFF_MD5 + 32] = MD5_PROXY_V2

# (c) génération : terrain10 -> terrain11 (dernier caractère)
img[OFF_L00] = ord("1")
img[OFF_S00] = ord("1")

# (d) VERSIONINFO binaire 0.5.11.0
struct.pack_into("<H", img, 0x5CD4, 11)
struct.pack_into("<H", img, 0x5CDC, 11)

# (e) chaîne FileVersion « 0.5.10 » -> « 0.5.11 » (utf-16, dernier char)
img[0x5DC2:0x5DC4] = "1".encode("utf-16-le")

# (f) chaîne ProductVersion « …terrain10 » -> « …terrain11 » (dernier char)
img[0x5ECC:0x5ECE] = "1".encode("utf-16-le")

# (g) sommes R10[23], R10[25], R10[26] recalculées sur l'image finale
for k in (23, 25, 26):
    rva_k, ln_k, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(img, rva_k, ln_k))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné (proxy + md5 + génération + .rsrc + 3 sommes)
autorisations = [
    (OFF_PROXY, OFF_PROXY + TAILLE_PROXY, "proxy v2 in-place"),
    (OFF_MD5, OFF_MD5 + 32, "chaîne md5"),
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
      f"(proxy ~1740 + md5 32 + génération 2 + .rsrc 6 + sommes 24)")

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

# 3c. le kit embarqué : demo + annexe INTACTS, proxy == m3/proxy.exe
if img[0x6400:OFF_PROXY] != base[0x6400:OFF_PROXY]:
    erreur("l'en-tête kit + demo.10 ont bougé")
if img[OFF_PROXY + TAILLE_PROXY:] != base[OFF_PROXY + TAILLE_PROXY:]:
    erreur("l'annexe jetons a bougé")
if bytes(img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY]) != proxy_v2:
    erreur("le proxy embarqué != m3/proxy.exe")
print("[blob] en-tête kit + demo.10 + annexe jetons inchangés ; "
      "proxy embarqué == m3/proxy.exe (md5 dd12b649…) octet pour octet")

# 3d. le md5 S05C journalisé
if bytes(img[OFF_MD5:OFF_MD5 + 32]) != MD5_PROXY_V2:
    erreur("md5 S05C final inattendu")
print("[md5] S05C journalisera dd12b64948e64153ff1dd7a66f367ff3")

# 3e. identité
if bytes(img[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain11" or bytes(img[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain11":
    erreur("versions L00/S00 finales inattendues")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", img, off_b)[0] != 11:
        erreur(f"VERSIONINFO finale inattendue @{off_b:#x}")
fv = img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0]
if fv != "0.5.11":
    erreur(f"FileVersion finale inattendue : {fv!r}")
pv = img[0x5EC0:0x5ECE].decode("utf-16-le")
if pv != "rrain11":
    erreur(f"ProductVersion (fin) inattendue : {pv!r}")
print("[ident] L00/S00 « terrain11 », VERSIONINFO 0.5.11.0, "
      "FileVersion « 0.5.11 », ProductVersion « …terrain11 »")

# 3f. le prologue du proxy embarqué (le probing, désassemblé)
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    # .text2 du proxy : rva 0x5580 -> fichier 0x2C00 + (0x5580 - 0x4000)
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
        for i, (a, b) in enumerate(zip(obtenu, attendu)):
            if a != b:
                print(f"  divergence @{i}: {a!r} != {b!r}")
        erreur("prologue http-10 embarqué inattendu")
    print("[code] prologue http-10 embarqué : push×5 ; BOUCLE DE PROBING "
          "([rsp-0x1000]…[rsp-0x7000], touche finale [rsp-0x7100]) ; sub rsp,0x7100")
except ImportError:
    print("[code] capstone absent (FAIBLE)")

# 3g. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
