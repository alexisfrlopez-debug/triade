#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.6 — la fenêtre du superviseur fermait avant la fin : CORRECTIF
FindWindowW (recherche par CLASSE, plus par titre) + version 0.5.6.0.

CONSTAT TERRAIN (terrain_20261027_165217.txt, le run terrain.5 de 16:52) :
  L00→L03 ✓, S00→S06 ✓ (l'annexe, demo.exe, proxy.exe extraits et conformes),
  puis S10 « lancement demo.exe », S11 « fenetre demo ABSENTE » — la fenêtre
  EXISTAIT (le journal demo_journal.txt du run montre L01 « fenetre principale
  creee » ET L03 « clic » manuel du développeur : la fenêtre était là,
  affichée, cliquable) — le superviseur CHERCHAIT MAL.

LA CAUSE (preuve binaire, 3 cordes) :
  1. sup-33 appelle FindWindowW(lpClassName=NULL, lpWindowName='TRIADE_demo')
     — il passe le NOM DE CLASSE en TITRE. Or demo.exe (embarqué, md5
     73c064fb) crée sa fenêtre avec CLASSE='TRIADE_demo' (@rva 0x29c0) et
     TITRE='TRIADE M2 — démonstration complète' (@rva 0x29d8). Aucune
     fenêtre ne porte le TITRE 'TRIADE_demo' : 200 sondes × 50 ms échouent,
     S11, puis le scénario TUE le demo (TerminateProcess) au 10e seconde —
     le run manuel du développeur coupé en pleine démonstration.
  2. Le journal demo s'arrête à « réseau : échange en échec » : l'échange
     du demo.9 (sondes retirées en D43) a échoué sur machine réelle AVANT
     le tueur — terrain.6 rejouera T1 automatiquement (fenêtre trouvée en
     < 1 s, clic BM_CLICK envoyé par le superviseur) : si l'échec persiste,
     le journal T1 le dira proprement, sans tueur ni main humaine.
  3. Après S21 (bannière proxy), la MORT au premier .curl : le scénario
     tourne sur un FIL (tcp-06) — la fenêtre répond — la fermeture ne peut
     venir que d'un WM_QUIT (croix fermée pendant les ~25 s de silence de
     l'attente curl --max-time 20) ou d'une terminaison externe (antivirus,
     cf. Wacatax.C!ml). terrain.6 identifie sa version DANS le journal
     (L00/S00 « terrain.6 ») pour trancher au prochain run.

LE CORRECTIF (patch chirurgical data+code MINIMAL, tout borné) :
  1. sup-33 @0x544f : 9 octets — « xor ecx,ecx ; lea rdx,[titre] » devient
     « lea rcx,[classe] ; xor edx,edx » — MÊME taille, MÊME chaîne
     ('TRIADE_demo' @0x2a92, maintenant lue comme lpClassName) :
     FindWindowW(L"TRIADE_demo", NULL) — la recherche par CLASSE, comme
     la fenêtre du demo l'exige ;
  2. somme R10 entrée [19] (bloc sup-33 0x5400+0x3C0) ajustée du delta
     exact — les 19 autres entrées recalculées VERTES à l'identique ;
  3. L00 (.rdata @0x2ada) et S00 (.text2 @0x4366) : « terrain.3 » ->
     « terrain.6 » (même longueur, un octet chacun — zones NON couvertes
     par R10, vérifié : aucune entrée ne les couvre) ;
  4. VERSIONINFO 0.5.5.0 -> 0.5.6.0 (4 champs, traçabilité WER).

AUCUN autre octet ne bouge : importations, .blob (demo.exe/proxy.exe
embarqués), en-têtes PE, IAT — intacts. La porte R10 reste VERTE.
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/home/z/my-project/upload/superviseur-terrain5.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain6.exe")

MD5_TERRAIN5 = "6ddfe8c2f9413031d792ec30bb9a0b9c"

# --- géométrie PE -----------------------------------------------------------
RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450
N_ENTREES_R10 = 20
ENTREE_SUP33 = 19                    # rva=0x5400 len=0x3C0 (bloc sup-33)

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
    """Somme tronquée de mots u64 LE — l'algorithme exact de la porte R10."""
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)

# =============================================================================
# 1. GARDES-FOUS sur terrain.5 (le binaire source doit être EXACTEMENT attendu)
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(base).hexdigest() != MD5_TERRAIN5:
    erreur("terrain.5 : md5 inattendu")

# 1a. les 9 octets à patcher @rva 0x544f (file 0x424f)
OFF_SUP33 = rva2off(0x544F)
ANCIEN_9 = bytes.fromhex("31c9488d153ad6ffff")
if bytes(base[OFF_SUP33:OFF_SUP33 + 9]) != ANCIEN_9:
    erreur(f"sup-33 @0x544f : octets inattendus {bytes(base[OFF_SUP33:OFF_SUP33+9]).hex()}")

# 1b. le call FindWindowW juste après (intact)
if bytes(base[OFF_SUP33 + 9:OFF_SUP33 + 15]) != bytes.fromhex("ff1502cfffff"):
    erreur("le call [rip-0x30fe] (FindWindowW @0x2360) après le lea a bougé")

# 1c. la chaîne de recherche 'TRIADE_demo' (UTF-16) @rva 0x2a92
OFF_STR = rva2off(0x2A92)
if base[OFF_STR:OFF_STR + 24] != "TRIADE_demo\0".encode("utf-16-le"):
    erreur("la chaîne UTF-16 'TRIADE_demo' @0x2a92 est introuvable")

# 1d. la porte R10 VERTE sur terrain.5 (les 20 entrées recalculées)
table_off = rva2off(R10_TABLE_RVA)
for k in range(N_ENTREES_R10):
    rva, ln, sm = struct.unpack_from("<IIQ", base, table_off + 16 * k)
    if not ln or rva2off(rva) is None:
        erreur(f"entrée R10[{k}] illisible : rva={rva:#x} len={ln:#x}")
    if somme_zone(base, rva, ln) != sm:
        erreur(f"porte R10 ROUGE sur terrain.5 à l'entrée [{k}]")
ent19_rva, ent19_len, ent19_somme = struct.unpack_from("<IIQ", base, table_off + 16 * ENTREE_SUP33)
if (ent19_rva, ent19_len) != (0x5400, 0x3C0):
    erreur(f"entrée R10[{ENTREE_SUP33}] : ce n'est pas le bloc sup-33")

# 1e. les octets de version L00/S00 ('3' final de « terrain.3 »)
OFF_L00_3 = rva2off(0x2ADA)
OFF_S00_3 = rva2off(0x4366)
if base[OFF_L00_3 - 8:OFF_L00_3 + 1] != b"terrain.3" or base[OFF_L00_3 + 1:OFF_L00_3 + 4] != b"L01":
    erreur("L00 @0x2ad2 : contexte inattendu")
if base[OFF_S00_3 - 8:OFF_S00_3 + 1] != b"terrain.3" or base[OFF_S00_3 + 1:OFF_S00_3 + 4] != b"S01":
    erreur("S00 @0x435e : contexte inattendu")

# 1f. aucune entrée R10 ne couvre L00 (0x2ad2) ni S00 (0x435e) — ni la table elle-même
for k in range(N_ENTREES_R10):
    rva, ln, sm = struct.unpack_from("<IIQ", base, table_off + 16 * k)
    for point in (0x2AD2, 0x435E, R10_TABLE_RVA):
        if rva <= point < rva + ln:
            erreur(f"R10[{k}] couvre {point:#x} — hypothèse violée, ajuster le plan")

# 1g. VERSIONINFO : les 4 champs attendus à 5 (0.5.5.0)
if struct.unpack_from("<H", base, 0x5CD4)[0] != 5:
    erreur("FileVersion binaire @0x5cd4 != 5")
if struct.unpack_from("<H", base, 0xCDC + 0x5000)[0] != 5:  # 0x5cdc
    erreur("ProductVersion binaire @0x5cdc != 5")
if base[0x5DC4:0x5DC6] != "5".encode("utf-16-le"):
    erreur("FileVersion chaîne @0x5dc4 != '5'")
if base[0x5ECC:0x5ECE] != "5".encode("utf-16-le"):
    erreur("ProductVersion chaîne @0x5ecc != '5'")

# =============================================================================
# 2. LE PATCH (copie -> écritures bornées)
# =============================================================================
img = bytearray(base)

# (a) sup-33 : FindWindowW(L"TRIADE_demo", NULL) — 9 octets, même taille
#     lea rcx, [rip - 0x29c4]  (= 0x2a92) ; xor edx, edx
NOUVEAU_9 = bytes.fromhex("488d0d3cd6ffff31d2")
img[OFF_SUP33:OFF_SUP33 + 9] = NOUVEAU_9

# (b) somme R10[19] ajustée (delta exact du mot u64 contenant 0x544f)
nouvelle_somme = somme_zone(img, ent19_rva, ent19_len)
struct.pack_into("<Q", img, table_off + 16 * ENTREE_SUP33 + 8, nouvelle_somme)

# (c) L00 / S00 : « terrain.3 » -> « terrain.6 » (un octet chacun, même longueur)
img[OFF_L00_3] = ord("6")
img[OFF_S00_3] = ord("6")

# (d) VERSIONINFO 0.5.5.0 -> 0.5.6.0 (4 champs)
struct.pack_into("<H", img, 0x5CD4, 6)                # FileVersion binaire
struct.pack_into("<H", img, 0x5CDC, 6)                # ProductVersion binaire
img[0x5DC4:0x5DC6] = "6".encode("utf-16-le")          # FileVersion chaîne
img[0x5ECC:0x5ECE] = "6".encode("utf-16-le")          # ProductVersion chaîne

# =============================================================================
# 3. POST-VÉRIFICATIONS (fail-closed)
# =============================================================================
# 3a. diff octet à octet : seules les zones autorisées bougent
autorisees = [
    (OFF_SUP33, OFF_SUP33 + 9),                                   # sup-33 lea/xor
    (table_off + 16 * ENTREE_SUP33 + 8,
     table_off + 16 * ENTREE_SUP33 + 16),                         # somme R10[19]
    (OFF_L00_3, OFF_L00_3 + 1),                                   # L00 '6'
    (OFF_S00_3, OFF_S00_3 + 1),                                   # S00 '6'
    (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),                           # versions binaires
    (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE),                           # versions chaînes
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorisees)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous dans les zones autorisées")

# 3b. la porte R10 VERTE sur l'image patchée (20/20 recalculés)
for k in range(N_ENTREES_R10):
    rva, ln, sm = struct.unpack_from("<IIQ", img, table_off + 16 * k)
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
print("[porte] R10 20/20 VERTES sur l'image patchée")

# 3c. le code patché se désassemble exactement comme prévu
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    code = bytes(img[OFF_SUP33:OFF_SUP33 + 15])
    attendu = ["lea rcx, [rip - 0x29c4]", "xor edx, edx",
               "call qword ptr [rip - 0x30fe]"]
    obtenu = [f"{i.mnemonic} {i.op_str}" for i in md.disasm(code, 0x544F)]
    if obtenu != attendu:
        erreur(f"désassemblage inattendu : {obtenu}")
    print(f"[code] 0x544f : {' ; '.join(attendu)}  (= FindWindowW(L\"TRIADE_demo\", NULL))")
except ImportError:
    print("[code] capstone absent — vérification désassemblage sautée (FAIBLE)")

# 3d. les sections critiques inchangées : en-têtes PE + .blob + descripteurs
for a, b in ((0, 0x400), (0x6400, len(img))):          # en-têtes + tout après .text2
    if any(base[i] != img[i] for i in range(a, b) if not any(
            x <= i < y for x, y in [(0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
                                    (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE)])):
        erreur(f"zone critique [{a:#x}..{b:#x}] modifiée hors VERSIONINFO")
print("[zones] en-têtes PE, .blob (demo/proxy embarqués), .idata : intacts")

# 3e. md5 final
final = hashlib.md5(bytes(img)).hexdigest()
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {hashlib.sha256(bytes(img)).hexdigest()}")
